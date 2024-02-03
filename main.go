package main

import (
	"digisign-backend/models"
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	router.GET("/pdfs", listpdfsHandler)
	router.POST("/pdfs", createpdfHandler)
	router.GET("/pdfs/:id", getpdfbyid)
	router.Run("localhost:8080")
}

func listpdfsHandler(c *gin.Context) {
	pdfs := models.ListPdfsHandler()
	if pdfs == nil || len(pdfs) == 0 {
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.IndentedJSON(http.StatusOK, pdfs)
	}
}

func createpdfHandler(c *gin.Context) {
	var pdf models.Pdf
	if err := c.BindJSON(&pdf); err != nil {
		c.AbortWithStatus(http.StatusBadRequest)
	} else {
		models.CreatePdfHandler(pdf)
		c.IndentedJSON(http.StatusCreated, pdf)
	}
}

func getpdfbyid(c *gin.Context) {
	id := c.Param("id")
	pdf := models.GetPdfById(id)

	if pdf == nil {
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.IndentedJSON(http.StatusOK, pdf)
	}
}
