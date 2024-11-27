package main

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/internal/application"
	"github.com/mezni/bridge/tools/cdrgen/internal/domain"
	"github.com/mezni/bridge/tools/cdrgen/internal/infrastructure"
)

func main() {
	// Initialize the logger (using SlogLogger)
	logger := infrastructure.NewSlogLogger()

	// Define the module name
	module := "MyModule"
	ctx := context.Background()

	// Initialize logger with context and module
	logger.Init(ctx, module)

	// Initialize the dummy service
	//	dummyService := domain.NewDummyService(logger)

	// Create the application service
	//	appService := application.NewApplicationService(dummyService, logger)

	// Start and stop the service
	//	appService.StartService(ctx, module)
	//	appService.StopService(ctx, module)
}
