use cxx::UniquePtr;
use std::cell::UnsafeCell;
use std::fmt;
use std::path::Path;

use crate::error::Error;
use crate::ffi::ffi;

/// The Database class is the main class of KuzuDB. It manages all database components.
pub struct Database {
    pub(crate) db: UnsafeCell<UniquePtr<ffi::Database>>,
}

unsafe impl Send for Database {}
unsafe impl Sync for Database {}

#[derive(Clone, Debug)]
/// Configuration options for the database.
pub struct SystemConfig {
    /// Max size of the buffer pool in bytes
    ///
    /// The larger the buffer pool, the more data from the database files is kept in memory,
    /// reducing the amount of File I/O.
    ///
    /// Defaults to an auto-detected size
    buffer_pool_size: u64,
    /// The maximum number of threads to use when executing queries
    /// Defaults to auto-detect from the number of processors
    max_num_threads: u64,
    /// When true, new columns will be compressed if possible
    /// Defaults to true
    enable_compression: bool,
    /// Whether or not the database can be written to from this instance
    /// Defaults to not read-only
    read_only: bool,
    /// The maximum size of the database. Defaults to 8TB
    max_db_size: u64,
}

impl Default for SystemConfig {
    fn default() -> SystemConfig {
        SystemConfig {
            buffer_pool_size: 0,
            max_num_threads: 0,
            enable_compression: true,
            read_only: false,
            // This is a little weird, but it's a temporary interface
            max_db_size: u32::MAX as u64,
        }
    }
}

impl SystemConfig {
    pub fn buffer_pool_size(mut self, buffer_pool_size: u64) -> Self {
        self.buffer_pool_size = buffer_pool_size;
        self
    }
    pub fn max_num_threads(mut self, max_num_threads: u64) -> Self {
        self.max_num_threads = max_num_threads;
        self
    }
    pub fn enable_compression(mut self, enable_compression: bool) -> Self {
        self.enable_compression = enable_compression;
        self
    }
    pub fn read_only(mut self, read_only: bool) -> Self {
        self.read_only = read_only;
        self
    }
    pub fn max_db_size(mut self, max_db_size: u64) -> Self {
        self.max_db_size = max_db_size;
        self
    }
}

pub(crate) const IN_MEMORY_DB_NAME: &str = ":memory:";

impl Database {
    /// Creates a database object
    ///
    /// # Arguments:
    /// * `path`: Path of the database. If the database does not already exist, it will be created.
    ///           If the path is empty, or equal to `:memory:`, the database will be created
    ///           in-memory.
    /// * `config`: Database configuration to use
    pub fn new<P: AsRef<Path>>(path: P, config: SystemConfig) -> Result<Self, Error> {
        Ok(Database {
            db: UnsafeCell::new(ffi::new_database(
                ffi::StringView::new(&path.as_ref().display().to_string()),
                config.buffer_pool_size,
                config.max_num_threads,
                config.enable_compression,
                config.read_only,
                config.max_db_size,
            )?),
        })
    }

    /// Creates an in-memory database
    ///
    /// Alias for `Database::new(":memory:", config)`
    pub fn in_memory(config: SystemConfig) -> Result<Self, Error> {
        Self::new(IN_MEMORY_DB_NAME, config)
    }
}

impl fmt::Debug for Database {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("Database")
            .field("db", &"Opaque C++ data".to_string())
            .finish()
    }
}

#[cfg(test)]
mod tests {
    use anyhow::{Error, Result};

    use crate::connection::Connection;
    use crate::database::{Database, SystemConfig};
    use std::collections::HashSet;

    #[test]
    fn create_database() -> Result<()> {
        let temp_dir = tempfile::tempdir()?;
        let _db = Database::new(temp_dir.path(), SystemConfig::default())?;
        temp_dir.close()?;
        Ok(())
    }

    #[test]
    fn create_database_no_compression() -> Result<()> {
        let temp_dir = tempfile::tempdir()?;
        let _ = Database::new(
            temp_dir.path(),
            SystemConfig::default().enable_compression(false),
        )?;
        temp_dir.close()?;
        Ok(())
    }

    #[test]
    fn test_database_read_only() -> Result<()> {
        let temp_dir = tempfile::tempdir()?;
        // Create database first so that it can be opened read-only
        {
            Database::new(temp_dir.path(), SystemConfig::default())?;
        }
        let db = Database::new(temp_dir.path(), SystemConfig::default().read_only(true))?;
        let conn = Connection::new(&db)?;
        let result: Error = conn
            .query("CREATE NODE TABLE Person(name STRING, age INT64, PRIMARY KEY(name));")
            .expect_err("Write query should produce an error on a read-only DB")
            .into();

        assert_eq!(
            result.to_string(),
            "Query execution failed: Cannot execute write operations in a read-only database!"
        );
        Ok(())
    }

    #[test]
    fn test_database_max_size() -> Result<()> {
        let temp_dir = tempfile::tempdir()?;
        {
            // Max DB size of 4GB should be fine
            Database::new(
                temp_dir.path(),
                SystemConfig::default().max_db_size(1 << 32),
            )?;
        }
        {
            Database::new(temp_dir.path(), SystemConfig::default().max_db_size(0))
                .expect_err("0 is not a valid max DB size");
        }
        Ok(())
    }

    #[test]
    fn test_database_in_memory() -> Result<()> {
        use crate::Value;
        let db = Database::in_memory(SystemConfig::default())?;
        // If the special name is ever changed (or removed) kuzu is likely to just create a db directory with that name
        assert!(!std::path::Path::new(crate::database::IN_MEMORY_DB_NAME).exists());

        let conn = Connection::new(&db)?;
        conn.query("CREATE NODE TABLE Person(name STRING, age INT64, PRIMARY KEY(name))");
        conn.query("BEGIN TRANSACTION")?;
        conn.query("CREATE (:Person {name: 'Alice', age: 25})")?;
        conn.query("CREATE (:Person {name: 'Bob', age: 30})")?;
        conn.query("COMMIT")?;
        let results: HashSet<String> = conn
            .query("MATCH (p:Person) RETURN p.name")?
            .map(|tuple| {
                assert!(tuple.len() == 1);
                if let Value::String(value) = &tuple[0] {
                    value.clone()
                } else {
                    panic!(
                        "Expected query values to be strings, but got {:?} instead",
                        tuple[0]
                    )
                }
            })
            .collect();
        assert!(results == HashSet::from(["Alice".to_string(), "Bob".to_string()]));
        Ok(())
    }
}
