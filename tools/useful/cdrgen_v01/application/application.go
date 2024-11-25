package application

import (
	"fmt"
	"github.com/mezni/bridge/tools/cdrgen/infrastructure"
	"github.com/spf13/cobra"
	"log"
)

// Application handles the business logic for loading config and starting services.
type Application struct {
	Logger *logger.Logger
	Config *domain.Config
}

// NewApplication creates a new instance of the Application service.
func NewApplication(config *domain.Config, logger *logger.Logger) *Application {
	return &Application{
		Logger: logger,
		Config: config,
	}
}

// LoadConfig loads the configuration from the specified file path.
func (app *Application) LoadConfig(filePath string) error {
	config, err := yamlparser.ParseYAMLConfig(filePath)
	if err != nil {
		return err
	}
	app.Config = config
	app.Logger.Info("Loaded configuration", "version", config.App.Version)
	return nil
}

// Run starts the necessary services.
func (app *Application) Run() {
	// Initialize and run the dummy service
	service := &domain.DummyService{Logger: app.Logger}
	if err := service.Start(); err != nil {
		app.Logger.Error("Error starting service", "error", err)
	}
}

// NewRootCmd creates the root command for the CLI.
func NewRootCmd(app *Application) *cobra.Command {
	rootCmd := &cobra.Command{
		Use:     "myprogram",
		Short:   "My program does amazing things",
		Version: app.Config.App.Version,
		RunE: func(cmd *cobra.Command, args []string) error {
			filePath, err := cmd.Flags().GetString("file")
			if err != nil {
				return fmt.Errorf("Error retrieving file flag: %w", err)
			}

			if err := app.LoadConfig(filePath); err != nil {
				return fmt.Errorf("Error loading config: %w", err)
			}

			app.Run()
			return nil
		},
	}

	// Add flags
	rootCmd.Flags().StringP("file", "f", "", "Path to YAML file (required)")
	if err := rootCmd.MarkFlagRequired("file"); err != nil {
		app.Logger.Error("Failed to mark flag as required", "error", err)
		log.Fatalf("Failed to mark flag as required: %v", err)
	}

	return rootCmd
}
