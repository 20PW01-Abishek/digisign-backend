//handlers/pdf_handlers.go
package handlers

import (
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

// CreatePDFHandler uploads a new PDF.
func CreatePDFHandler(c *gin.Context) {

}

// gets PDF by supplying id.
func GetPDFByIDHandler(c *gin.Context) {
}
