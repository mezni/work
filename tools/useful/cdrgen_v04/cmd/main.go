package main

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/internal/application"
	"github.com/mezni/bridge/tools/cdrgen/internal/domain/services"
	"github.com/mezni/bridge/tools/cdrgen/internal/infrastructure/logger"
)

func main() {
	contextData := make(map[any]any)
	ctx := context.WithValue(context.Background(), "context", contextData)
	contextData[logger.CustomContextKey("requestID")] = "12345"
	logger := logger.NewSlogLogger(logger.InfoLevel, "myModule", ctx)
	logger.Info("Start")

	dummyService := services.NewDummyService(logger)

	// Create an application service that uses the DummyService
	dummyServiceApp := application.NewDummyServiceApp(dummyService)

	// Execute the dummy service method (which does nothing)
	dummyServiceApp.ExecuteDummyService()
	logger.Debug("Stop")
}
