package main

import (
	"log"
	"github.com/mezni/bridge/tools/cdrgen/application"
	"github.com/mezni/bridge/tools/cdrgen/infrastructure"
	"github.com/mezni/bridge/tools/cdrgen/domain"
)

func main() {
	// Create a logger and application instances
	logger := logger.NewLogger("myprogram")

	config := &domain.Config{}
	app := application.NewApplication(config, logger)

	// Create and execute the root command
	rootCmd := command.NewRootCmd(app)
	if err := rootCmd.Execute(); err != nil {
		logger.Error("Error executing root command", "error", err)
		log.Fatalf("Error executing root command: %v", err)
	}
}
