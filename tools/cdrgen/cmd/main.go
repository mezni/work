package main

import (
	"fmt"
	"log"
	"github.com/spf13/cobra"
	"time"
)

// DummyService represents a service that does nothing
type DummyService struct{}

// Start simulates starting the service (does nothing)
func (d *DummyService) Start() {
	fmt.Println("DummyService started...")
	// Simulate doing nothing, for example, wait a few seconds
	time.Sleep(3 * time.Second)
	fmt.Println("DummyService finished doing nothing.")
}

// NewRootCmd creates the root command for the application
func NewRootCmd(programName, version string) *cobra.Command {
	rootCmd := &cobra.Command{
		Use:     programName, // Use the program name passed as an argument
		Short:   "My program does amazing things",
		Version: version, // Use the version passed as an argument
		Run:     run,
	}

	// Add flags
	rootCmd.Flags().StringP("file", "f", "", "Path to YAML file (required)")
	err := rootCmd.MarkFlagRequired("file")
	if err != nil {
		log.Fatalf("Failed to mark flag as required: %v", err)
	}

	return rootCmd
}

func run(cmd *cobra.Command, args []string) {
	filePath, err := cmd.Flags().GetString("file")
	if err != nil {
		log.Fatalf("Error retrieving file flag: %v", err)
	}

	// Print the file path from the flag
	fmt.Printf("File path: %s\n", filePath)

	// Initialize and start the dummy service
	dummyService := &DummyService{}
	dummyService.Start()
}

// main function to execute the Cobra command
func main() {
	// Define the program name and version directly as variables
	programName := "cdrgen" // The name of your program
	version := "0.0.1"         // This can be a constant, or set dynamically at build time

	// Create the root command with the program name and version
	rootCmd := NewRootCmd(programName, version)

	// Execute the root command
	if err := rootCmd.Execute(); err != nil {
		log.Fatalf("Error executing root command: %v", err)
	}
}
