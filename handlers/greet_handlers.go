// /handlers/greet_handlers.go

package handlers

import(
	"net/http"
	"github.com/gin-gonic/gin"
)

func GreetCreators(c *gin.Context){
	c.String(http.StatusOK, "Hello, Karthik and Abishek!")
}