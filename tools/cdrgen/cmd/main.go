package main

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/internal/infrastructure/logger"
)



func main() {
	// Create a map to hold context key-value pairs
	contextData := make(map[any]any)
	contextData[logger.CustomContextKey("requestID")] = "12345"
	contextData[logger.CustomContextKey("userID")] = 789

	// Initialize the context with multiple key-value pairs
	ctx := context.WithValue(context.Background(), "context", contextData)

	// Example usage of the logger with context
	loggerWithContext := logger.NewSlogLogger(logger.InfoLevel, "HTTPServer", ctx)
	loggerWithContext.Debug("This is a debug message", "key1", "debug_value") // Debug level logs

	// Example usage of the logger without context
	loggerWithoutContext := logger.NewSlogLogger(logger.InfoLevel, "HTTPServer")
	loggerWithoutContext.Info("This is an info message", "key1", "value1") // Info level logs
}
