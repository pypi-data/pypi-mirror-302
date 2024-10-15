#include "optimizer/projection_push_down_optimizer.h"

#include "binder/expression_visitor.h"
#include "common/cast.h"
#include "planner/operator/extend/logical_extend.h"
#include "planner/operator/extend/logical_recursive_extend.h"
#include "planner/operator/logical_accumulate.h"
#include "planner/operator/logical_filter.h"
#include "planner/operator/logical_hash_join.h"
#include "planner/operator/logical_intersect.h"
#include "planner/operator/logical_order_by.h"
#include "planner/operator/logical_projection.h"
#include "planner/operator/logical_unwind.h"
#include "planner/operator/persistent/logical_copy_from.h"
#include "planner/operator/persistent/logical_delete.h"
#include "planner/operator/persistent/logical_insert.h"
#include "planner/operator/persistent/logical_merge.h"
#include "planner/operator/persistent/logical_set.h"

using namespace kuzu::common;
using namespace kuzu::planner;
using namespace kuzu::binder;

namespace kuzu {
namespace optimizer {

void ProjectionPushDownOptimizer::rewrite(planner::LogicalPlan* plan) {
    visitOperator(plan->getLastOperator().get());
}

void ProjectionPushDownOptimizer::visitOperator(LogicalOperator* op) {
    visitOperatorSwitch(op);
    if (op->getOperatorType() == LogicalOperatorType::PROJECTION) {
        // We will start a new optimizer once a projection is encountered.
        return;
    }
    // top-down traversal
    for (auto i = 0u; i < op->getNumChildren(); ++i) {
        visitOperator(op->getChild(i).get());
    }
    op->computeFlatSchema();
}

void ProjectionPushDownOptimizer::visitPathPropertyProbe(planner::LogicalOperator* op) {
    auto pathPropertyProbe = (LogicalPathPropertyProbe*)op;
    KU_ASSERT(
        pathPropertyProbe->getChild(0)->getOperatorType() == LogicalOperatorType::RECURSIVE_EXTEND);
    auto recursiveExtend = (LogicalRecursiveExtend*)pathPropertyProbe->getChild(0).get();
    auto boundNodeID = recursiveExtend->getBoundNode()->getInternalID();
    collectExpressionsInUse(boundNodeID);
    auto rel = recursiveExtend->getRel();
    if (!patternInUse.contains(rel)) {
        pathPropertyProbe->setJoinType(planner::RecursiveJoinType::TRACK_NONE);
        recursiveExtend->setJoinType(planner::RecursiveJoinType::TRACK_NONE);
    }
}

void ProjectionPushDownOptimizer::visitExtend(planner::LogicalOperator* op) {
    auto extend = (LogicalExtend*)op;
    auto boundNodeID = extend->getBoundNode()->getInternalID();
    collectExpressionsInUse(boundNodeID);
}

void ProjectionPushDownOptimizer::visitAccumulate(planner::LogicalOperator* op) {
    auto accumulate = (LogicalAccumulate*)op;
    if (accumulate->getAccumulateType() != AccumulateType::REGULAR) {
        return;
    }
    auto expressionsBeforePruning = accumulate->getPayloads();
    auto expressionsAfterPruning = pruneExpressions(expressionsBeforePruning);
    if (expressionsBeforePruning.size() == expressionsAfterPruning.size()) {
        return;
    }
    preAppendProjection(op, 0, expressionsAfterPruning);
}

void ProjectionPushDownOptimizer::visitFilter(planner::LogicalOperator* op) {
    auto filter = (LogicalFilter*)op;
    collectExpressionsInUse(filter->getPredicate());
}

void ProjectionPushDownOptimizer::visitHashJoin(planner::LogicalOperator* op) {
    auto hashJoin = (LogicalHashJoin*)op;
    for (auto& [probeJoinKey, buildJoinKey] : hashJoin->getJoinConditions()) {
        collectExpressionsInUse(probeJoinKey);
        collectExpressionsInUse(buildJoinKey);
    }
    if (hashJoin->getJoinType() == JoinType::MARK) { // no need to perform push down for mark join.
        return;
    }
    auto expressionsBeforePruning = hashJoin->getExpressionsToMaterialize();
    auto expressionsAfterPruning = pruneExpressions(expressionsBeforePruning);
    if (expressionsBeforePruning.size() == expressionsAfterPruning.size()) {
        // TODO(Xiyang): replace this with a separate optimizer.
        return;
    }
    preAppendProjection(op, 1, expressionsAfterPruning);
}

void ProjectionPushDownOptimizer::visitIntersect(planner::LogicalOperator* op) {
    auto intersect = (LogicalIntersect*)op;
    collectExpressionsInUse(intersect->getIntersectNodeID());
    for (auto i = 0u; i < intersect->getNumBuilds(); ++i) {
        auto childIdx = i + 1; // skip probe
        auto keyNodeID = intersect->getKeyNodeID(i);
        collectExpressionsInUse(keyNodeID);
        // Note: we have a potential bug under intersect.cpp. The following code ensures build key
        // and intersect key always appear as the first and second column. Should be removed once
        // the bug is fixed.
        expression_vector expressionsBeforePruning;
        expression_vector expressionsAfterPruning;
        for (auto& expression :
            intersect->getChild(childIdx)->getSchema()->getExpressionsInScope()) {
            if (expression->getUniqueName() == intersect->getIntersectNodeID()->getUniqueName() ||
                expression->getUniqueName() == keyNodeID->getUniqueName()) {
                continue;
            }
            expressionsBeforePruning.push_back(expression);
        }
        expressionsAfterPruning.push_back(keyNodeID);
        expressionsAfterPruning.push_back(intersect->getIntersectNodeID());
        for (auto& expression : pruneExpressions(expressionsBeforePruning)) {
            expressionsAfterPruning.push_back(expression);
        }
        if (expressionsBeforePruning.size() == expressionsAfterPruning.size()) {
            return;
        }

        preAppendProjection(op, childIdx, expressionsAfterPruning);
    }
}

void ProjectionPushDownOptimizer::visitProjection(LogicalOperator* op) {
    // Projection operator defines the start of a projection push down until the next projection
    // operator is seen.
    ProjectionPushDownOptimizer optimizer;
    auto projection = (LogicalProjection*)op;
    for (auto& expression : projection->getExpressionsToProject()) {
        optimizer.collectExpressionsInUse(expression);
    }
    optimizer.visitOperator(op->getChild(0).get());
}

void ProjectionPushDownOptimizer::visitOrderBy(planner::LogicalOperator* op) {
    auto orderBy = (LogicalOrderBy*)op;
    for (auto& expression : orderBy->getExpressionsToOrderBy()) {
        collectExpressionsInUse(expression);
    }
    auto expressionsBeforePruning = orderBy->getChild(0)->getSchema()->getExpressionsInScope();
    auto expressionsAfterPruning = pruneExpressions(expressionsBeforePruning);
    if (expressionsBeforePruning.size() == expressionsAfterPruning.size()) {
        return;
    }
    preAppendProjection(op, 0, expressionsAfterPruning);
}

void ProjectionPushDownOptimizer::visitUnwind(planner::LogicalOperator* op) {
    auto unwind = (LogicalUnwind*)op;
    collectExpressionsInUse(unwind->getInExpr());
}

void ProjectionPushDownOptimizer::visitInsert(planner::LogicalOperator* op) {
    auto insert = (LogicalInsert*)op;
    for (auto& info : insert->getInfos()) {
        visitInsertInfo(info);
    }
}

void ProjectionPushDownOptimizer::visitDelete(planner::LogicalOperator* op) {
    auto delete_ = op->constPtrCast<LogicalDelete>();
    auto& infos = delete_->getInfos();
    KU_ASSERT(!infos.empty());
    switch (infos[0].tableType) {
    case TableType::NODE: {
        for (auto& info : infos) {
            auto& node = info.pattern->constCast<NodeExpression>();
            collectExpressionsInUse(node.getInternalID());
            for (auto entry : node.getEntries()) {
                collectExpressionsInUse(node.getPrimaryKey(entry->getTableID()));
            }
        }
    } break;
    case TableType::REL: {
        for (auto& info : infos) {
            auto& rel = info.pattern->constCast<RelExpression>();
            collectExpressionsInUse(rel.getSrcNode()->getInternalID());
            collectExpressionsInUse(rel.getDstNode()->getInternalID());
            collectExpressionsInUse(rel.getInternalIDProperty());
        }
    } break;
    default:
        KU_UNREACHABLE;
    }
}

void ProjectionPushDownOptimizer::visitMerge(planner::LogicalOperator* op) {
    auto merge = op->ptrCast<LogicalMerge>();
    collectExpressionsInUse(merge->getExistenceMark());
    for (auto& info : merge->getInsertNodeInfos()) {
        visitInsertInfo(info);
    }
    for (auto& info : merge->getInsertRelInfos()) {
        visitInsertInfo(info);
    }
    for (auto& info : merge->getOnCreateSetNodeInfos()) {
        visitSetInfo(info);
    }
    for (auto& info : merge->getOnMatchSetNodeInfos()) {
        visitSetInfo(info);
    }
    for (auto& info : merge->getOnCreateSetRelInfos()) {
        visitSetInfo(info);
    }
    for (auto& info : merge->getOnMatchSetRelInfos()) {
        visitSetInfo(info);
    }
}

void ProjectionPushDownOptimizer::visitSetProperty(planner::LogicalOperator* op) {
    auto set = op->ptrCast<LogicalSetProperty>();
    for (auto& info : set->getInfos()) {
        visitSetInfo(info);
    }
}

void ProjectionPushDownOptimizer::visitCopyFrom(planner::LogicalOperator* op) {
    auto copyFrom = ku_dynamic_cast<LogicalOperator*, LogicalCopyFrom*>(op);
    for (auto& expr : copyFrom->getInfo()->source->getColumns()) {
        collectExpressionsInUse(expr);
    }
    collectExpressionsInUse(copyFrom->getInfo()->offset);
}

void ProjectionPushDownOptimizer::visitSetInfo(const binder::BoundSetPropertyInfo& info) {
    switch (info.tableType) {
    case TableType::NODE: {
        auto& node = info.pattern->constCast<NodeExpression>();
        collectExpressionsInUse(node.getInternalID());
        if (info.updatePk) {
            collectExpressionsInUse(info.column);
        }
    } break;
    case TableType::REL: {
        auto& rel = info.pattern->constCast<RelExpression>();
        collectExpressionsInUse(rel.getSrcNode()->getInternalID());
        collectExpressionsInUse(rel.getDstNode()->getInternalID());
        collectExpressionsInUse(rel.getInternalIDProperty());
    } break;
    default:
        KU_UNREACHABLE;
    }
    collectExpressionsInUse(info.columnData);
}

void ProjectionPushDownOptimizer::visitInsertInfo(const planner::LogicalInsertInfo& info) {
    if (info.tableType == common::TableType::REL) {
        auto& rel = info.pattern->constCast<RelExpression>();
        collectExpressionsInUse(rel.getSrcNode()->getInternalID());
        collectExpressionsInUse(rel.getDstNode()->getInternalID());
        collectExpressionsInUse(rel.getInternalIDProperty());
    }
    for (auto i = 0u; i < info.columnExprs.size(); ++i) {
        if (info.isReturnColumnExprs[i]) {
            collectExpressionsInUse(info.columnExprs[i]);
        }
        collectExpressionsInUse(info.columnDataExprs[i]);
    }
}

// See comments above this class for how to collect expressions in use.
void ProjectionPushDownOptimizer::collectExpressionsInUse(
    std::shared_ptr<binder::Expression> expression) {
    if (expression->expressionType == ExpressionType::PROPERTY) {
        propertiesInUse.insert(std::move(expression));
        return;
    }
    if (expression->expressionType == ExpressionType::PATTERN) {
        patternInUse.insert(expression);
    }
    for (auto& child : ExpressionChildrenCollector::collectChildren(*expression)) {
        collectExpressionsInUse(child);
    }
}

binder::expression_vector ProjectionPushDownOptimizer::pruneExpressions(
    const binder::expression_vector& expressions) {
    expression_set expressionsAfterPruning;
    for (auto& expression : expressions) {
        switch (expression->expressionType) {
        case ExpressionType::PATTERN: {
            if (patternInUse.contains(expression)) {
                expressionsAfterPruning.insert(expression);
            }
        } break;
        case ExpressionType::PROPERTY: {
            if (propertiesInUse.contains(expression)) {
                expressionsAfterPruning.insert(expression);
            }
        } break;
        default: // We don't track other expression types so always assume they will be in use.
            expressionsAfterPruning.insert(expression);
        }
    }
    return expression_vector{expressionsAfterPruning.begin(), expressionsAfterPruning.end()};
}

void ProjectionPushDownOptimizer::preAppendProjection(planner::LogicalOperator* op,
    uint32_t childIdx, binder::expression_vector expressions) {
    if (expressions.empty()) {
        // We don't have a way to handle
        return;
    }
    auto projection =
        std::make_shared<LogicalProjection>(std::move(expressions), op->getChild(childIdx));
    projection->computeFlatSchema();
    op->setChild(childIdx, std::move(projection));
}

} // namespace optimizer
} // namespace kuzu
