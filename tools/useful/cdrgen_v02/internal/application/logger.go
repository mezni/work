package application

import (
	"context"
)

// Logger defines the common interface for logging with context and module
type Logger interface {
	Init(ctx context.Context, module string) Logger // Initialize the logger with context and module
	Info(msg string, args ...interface{})
	Error(msg string, args ...interface{})
	Debug(msg string, args ...interface{})
}
