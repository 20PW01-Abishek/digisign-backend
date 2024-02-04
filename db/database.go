// /db/database.go
package db

import (
    "fmt"
    "github.com/jmoiron/sqlx"
    _ "github.com/go-sql-driver/mysql"
)

var db *sqlx.DB

// ConnectDB connects to the MySQL database
func ConnectDB() (*sqlx.DB, error) {
    dataSourceName := "admin:sqladmin@tcp(127.0.0.1:3306)/digisign"
    db, err := sqlx.Connect("mysql", dataSourceName)
    if err != nil {
        return nil, fmt.Errorf("failed to connect to database: %v", err)
    }
    return db, nil
}

// CloseDB closes the database connection
func CloseDB() error {
    if db != nil {
        return db.Close()
    }
    return nil
}

// GetDB returns the database connection
func GetDB() *sqlx.DB {
    return db
}