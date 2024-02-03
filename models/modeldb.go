package models

import (
	"database/sql"

	_ "github.com/go-sql-driver/mysql"

	"fmt"
)

const dbuser = "root"
const dbname = "test"
const dbpassword = "root"

func ListPdfsHandler() []Pdf {
	// db, err := sql.Open("mysql", dbuser+"@tcp(127.0.0.1:3306)/"+dbname)
	dsn := fmt.Sprintf("%s:%s@tcp(localhost:3306)/%s", dbuser, dbpassword, dbname)
    db, err := sql.Open("mysql", dsn)

	if err != nil {
		fmt.Println("Err", err.Error())
		return nil
	}

	defer db.Close()

	results, err := db.Query("SELECT * FROM pdfs")

	if err != nil {
		fmt.Println("Err", err.Error())
		return nil

	}
	pdfs1 := []Pdf{}
	for results.Next() {
		var pdf Pdf
		err = results.Scan(&pdf.ID, &pdf.FileName, &pdf.UploaderID)

		if err != nil {
			panic(err.Error())
		}
		pdfs1 = append(pdfs1, pdf)
	}
	return pdfs1
}

func CreatePdfHandler(pdfs Pdf) {
	// db, err := sql.Open("mysql", dbuser+"@tcp(127.0.0.1:3306)/"+dbname)
	dsn := fmt.Sprintf("%s:%s@tcp(localhost:3306)/%s", dbuser, dbpassword, dbname)
    db, err := sql.Open("mysql", dsn)
	if err != nil {
		fmt.Println("Err", err.Error())
	}

	defer db.Close()
	insert, err := db.Query(
		"INSERT INTO pdfs (pdf_id,filename,uploader_id) VALUES (?,?,?)",
		pdfs.ID, pdfs.FileName, pdfs.UploaderID)

	if err != nil {
		fmt.Println("Err", err.Error())
	}
	defer insert.Close()
}

func GetPdfById(id string) *Pdf {
	// db, err := sql.Open("mysql", dbuser+"@tcp(127.0.0.1:3306)/"+dbname)
	dsn := fmt.Sprintf("%s:%s@tcp(localhost:3306)/%s", dbuser, dbpassword, dbname)
    db, err := sql.Open("mysql", dsn)
	mov := &Pdf{}
	if err != nil {
		fmt.Println("Err", err.Error())
		return nil
	}
	defer db.Close()

	results, err := db.Query("SELECT * FROM pdfs where pdf_id=?", id)

	if err != nil {
		fmt.Println("Err", err.Error())
		return nil
	}

	if results.Next() {
		err = results.Scan(&mov.ID, &mov.FileName, &mov.UploaderID)
		if err != nil {
			return nil
		}
	} else {
		return nil
	}
	return mov
}
