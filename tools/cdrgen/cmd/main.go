package main

import (
	"fmt"
	"github.com/mezni/bridge/tools/cdrgen/internal/domain"
	"github.com/mezni/bridge/tools/cdrgen/internal/infrastructure"
	"github.com/mezni/bridge/tools/cdrgen/internal/application"
)

func main() {
	// Initialize the logger with the module name

		logger := infrastructure.NewCustomLogger("MyModule")

	// Initialize the repository and service
	repo := infrastructure.NewSequenceRepository()
	sequenceService := service.NewSequenceService(repo, logger)

	// Create a few sequences
	seq1, _ := domain.NewSequence("Even Numbers", 0, 2)
	seq2, _ := domain.NewSequence("Odd Numbers", 1, 2)

	// Add sequences to the repository
	repo.Add(seq1)
	repo.Add(seq2)

	// Retrieve all sequences
	sequences, err := repo.GetAll()
	if err != nil {
		logger.Error("Error retrieving sequences", "error", err)
		return
	}

	// Print all sequences
	fmt.Println("All stored sequences:")
	for _, seq := range sequences {
		fmt.Printf("Name: %s, Start: %d, Step: %d\n", seq.Name, seq.Start, seq.Step)
	}

	// Generate a sequence using the SequenceService
	sequence, err := sequenceService.GenerateSequence(&seq1, 10)
	if err != nil {
		logger.Error("Error generating sequence", "error", err)
		return
	}

	// Print the generated sequence
	fmt.Println("Generated sequence:", sequence)
}
