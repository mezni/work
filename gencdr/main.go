package main

import (
	"fmt"
	"log"
	"github.com/mezni/bridge/gencdr/core"

)

func main() {
	// Create a new Repository
	repo := core.NewRepository()

	// Create a new DataMap with some sample data
	data := core.DataMap{
		"name":    "Alice",
		"active":  true,
		"balance": 100.50,
	}

	// Define the required keys
	requiredKeys := []string{"name", "active"}

	// Add a new record to the repository
	if err := repo.AddRecord(data, requiredKeys); err != nil {
		log.Println("Error adding record:", err)
	} else {
		fmt.Println("Record added successfully")
	}

	// Retrieve a record from the repository by ID
	for _, record := range repo.Records { // Access 'Records' directly now
		fmt.Println("Retrieved Record:", record)
	}
}

