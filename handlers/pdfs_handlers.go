//handlers/pdf_handlers.go
package handlers

import (
    "fmt"
    "io/ioutil"
	"log"
    "net/http"
	"digisign-backend/db"
    "github.com/gin-gonic/gin"
)

func ListPDFsHandler(c *gin.Context) {
	// fun. to be completed.
	db, err := db.ConnectDB()
    if err != nil {
        log.Fatalf("Failed to connect to database: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to connect to database"})
        return
    }
    defer db.Close()

    // Query the pdfs table
    rows, err := db.Query("SELECT * FROM pdfs")
    if err != nil {
        log.Fatalf("Failed to query pdfs table: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query pdfs table"})
        return
    }
    defer rows.Close()

	// Define a slice to hold PDF data
	var pdfs []map[string]interface{}

    // Iterate through the result set and build PDF objects
    for rows.Next() {
        var (
            pdfID      int
            filename   string
            uploaderID int
            uploadDate string
            pdfBlob    []byte
        )
        if err := rows.Scan(&pdfID, &filename, &uploaderID, &uploadDate, &pdfBlob); err != nil {
            log.Fatalf("Failed to scan row: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to scan row"})
            return
        }
		
		// Create a map to hold PDF data
		pdf := make(map[string]interface{})
		pdf["pdf_id"] = pdfID
		pdf["filename"] = filename
		pdf["uploader_id"] = uploaderID
		pdf["upload_date"] = uploadDate
		// You might not want to include the PDF blob in the response

		// Append the PDF data to the slice
		pdfs = append(pdfs, pdf)
		
        // fmt.Printf("PDF ID: %d, Filename: %s, Uploader ID: %d, Upload Date: %s\n", pdfID, filename, uploaderID, uploadDate)
    }
    if err := rows.Err(); err != nil {
        log.Fatalf("Error occurred during iteration: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error occurred during iteration"})
        return
    }

    // Return the list of PDFs as JSON response
    c.JSON(http.StatusOK, pdfs)
}

func CreatePDFHandler(c *gin.Context) {
	// Parse the incoming request to extract the PDF file
	file, _, err := c.Request.FormFile("pdf")
	if err != nil {
		log.Printf("Failed to parse PDF file: %v", err)
		c.JSON(http.StatusBadRequest, gin.H{"error": "Failed to parse PDF file"})
		return
	}
	defer file.Close()

	// Read the content of the PDF file
	pdfContent, err := ioutil.ReadAll(file)
	if err != nil {
		log.Printf("Failed to read PDF content: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to read PDF content"})
		return
	}

	// Connect to the database
	database, err := db.ConnectDB()
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to connect to database"})
		return
	}
	defer database.Close()

	// Insert the PDF content into the database
	insertQuery := "INSERT INTO pdfs (filename, uploader_id, pdf_blob) VALUES (?, ?, ?)"
	result, err := database.Exec(insertQuery, "example.pdf", 123, pdfContent)
	if err != nil {
		log.Printf("Failed to insert PDF into database: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to insert PDF into database"})
		return
	}

	// Get the ID of the inserted PDF
	pdfID, err := result.LastInsertId()
	if err != nil {
		log.Printf("Failed to get ID of inserted PDF: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get ID of inserted PDF"})
		return
	}

	// Return success response with ID of the inserted PDF
	c.JSON(http.StatusOK, gin.H{"message": fmt.Sprintf("PDF uploaded successfully with ID: %d", pdfID)})
}

// gets PDF by supplying id.
func GetPDFByIDHandler(c *gin.Context) {
}
