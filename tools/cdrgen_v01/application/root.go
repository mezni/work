package application

import (
	"fmt"
	"log"
	"os"

	"github.com/spf13/cobra"
)

// NewRootCmd creates the root command for the CLI, initializes the application, and runs it.
func NewRootCmd(app *application.Application) *cobra.Command {
	rootCmd := &cobra.Command{
		Use:     "myprogram",
		Short:   "My program does amazing things",
		Version: app.Config.App.Version, // Version from the loaded configuration
		RunE: func(cmd *cobra.Command, args []string) error {
			// Get the file path from the flag
			filePath, err := cmd.Flags().GetString("file")
			if err != nil {
				return fmt.Errorf("Error retrieving file flag: %w", err)
			}

			// Load the configuration
			if err := app.LoadConfig(filePath); err != nil {
				return fmt.Errorf("Error loading config: %w", err)
			}

			// Run the application logic
			app.Run()
			return nil
		},
	}

	// Define the flag for the file path (required)
	rootCmd.Flags().StringP("file", "f", "", "Path to YAML file (required)")
	if err := rootCmd.MarkFlagRequired("file"); err != nil {
		log.Fatalf("Failed to mark flag as required: %v", err)
	}

	return rootCmd
}
