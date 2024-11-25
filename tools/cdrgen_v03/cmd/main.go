package main

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/internal/application/services"
	"github.com/mezni/bridge/tools/cdrgen/internal/domain/services"
	"github.com/mezni/bridge/tools/cdrgen/internal/infrastructure/logger"
)

func main() {
	contextData := make(map[any]any)
	ctx := context.WithValue(context.Background(), "context", contextData)
	contextData[logger.CustomContextKey("requestID")] = "12345"
	logger := logger.NewSlogLogger(logger.InfoLevel, "myModule", ctx)
	logger.Info("This is an info message", "key1", "value1")
	logger.Debug("This is an info message", "key1", "value1")
	dummyService := domain.NewDummyService(logger)
	dummyServiceApp := application.NewDummyServiceApp(dummyService)

}
