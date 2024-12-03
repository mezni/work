package main

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/application"
	"github.com/mezni/bridge/tools/cdrgen/domain/services"
	"github.com/mezni/bridge/tools/cdrgen/infrastructure/logging"
	"github.com/mezni/bridge/tools/cdrgen/infrastructure/persistance/inmemory"
)

func main() {
	// Create a new logger instance
	logger := logging.NewSlogLogger("CdrGen")

	// Create a context with a request ID
	ctx := context.Background()
	ctx = context.WithValue(ctx, "requestID", "12345")

	// Generate IMSI and IMEI using the application layer
	application.GenerateIMSI(ctx, logger)
	application.GenerateIMEI(ctx, logger)
	application.GenerateMSISDN(ctx, logger)
	application.GenerateIP(ctx, logger)
	application.GenerateDatetime(ctx, logger)

	repo := inmemory.NewInMemorySequenceRepository()
	service := services.NewSequenceService(repo, logger)
	app := application.NewSequenceApplication(service, logger)
	ctx = context.WithValue(context.Background(), "requestID", "abc123")

	// Create a sequence
	err := app.CreateSequence(ctx, "order_id", 1000, 10)
	if err != nil {
		logger.Error(ctx, "Error creating sequence", "error", err)

	}

	// Generate the next value
	nextValue, err := app.GenerateNextValue(ctx, "order_id")
	if err != nil {
		logger.Error(ctx, "Error generating next value", "error", err)

	}
	logger.Info(ctx, "Next value", "value", nextValue)
}
