package main

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/internal/infrastructure/logger"
)



func main() {
	contextData := make(map[any]any)
ctx := context.WithValue(context.Background(), "context", contextData)
	logger := logger.NewSlogLogger(logger.InfoLevel, "myModule",ctx)
	logger.Info("This is an info message", "key1", "value1") 
	logger.Debug("This is an info message", "key1", "value1") 
}
