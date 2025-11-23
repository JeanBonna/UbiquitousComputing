package main

import (
	"GolangApi/database"
	"GolangApi/router"
	"log"
)

func main() {
	if err := database.InitDb(); err != nil {
		log.Fatalf("Failed to initialize database %w", err)
	}

	defer database.CloseDB()

	log.Println("Starting server on port 8080...")

	router.StartRouter()
}
