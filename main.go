// /main.go
package main

import (
	"github.com/gin-gonic/gin"
	"digisign-backend/handlers"
)

func main() {
	router := gin.Default()
	router.GET("/",handlers.GreetCreators)
    router.GET("/pdfs/list", handlers.ListPDFsHandler)
    router.POST("/pdfs/create", handlers.CreatePDFHandler)
    router.GET("/getpdf", handlers.GetPDFByIDHandler)
    router.Run("localhost:8080")
}