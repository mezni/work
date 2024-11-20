package main

import (
	"context"
	"fmt"
	"os"
	"time"
)

// Logger defines the interface for custom logging
type Logger interface {
	Enabled(ctx context.Context, level LogLevel) bool
	Log(ctx context.Context, level LogLevel, message string, attrs ...Attr)
}

// LogLevel defines the logging levels
type LogLevel int

const (
	LevelDebug LogLevel = iota
	LevelInfo
	LevelWarn
	LevelError
)

// Attr represents a key-value pair for logging attributes
type Attr struct {
	Key   string
	Value any
}

// SimpleLogger is an implementation of the Logger interface
type SimpleLogger struct{}

func (l *SimpleLogger) Enabled(ctx context.Context, level LogLevel) bool {
	// Enable all levels except debug
	// return level != LevelDebug
	return true
}

func (l *SimpleLogger) Log(ctx context.Context, level LogLevel, message string, attrs ...Attr) {
	if !l.Enabled(ctx, level) {
		return
	}

	timestamp := time.Now().Format(time.RFC3339)
	attrString := ""
	for _, attr := range attrs {
		attrString += fmt.Sprintf(" %s=%v", attr.Key, attr.Value)
	}

	switch level {
	case LevelDebug:
		fmt.Fprintf(os.Stderr, "[DEBUG] %s %s%s\n", timestamp, message, attrString)
	case LevelInfo:
		fmt.Fprintf(os.Stderr, "[INFO] %s %s%s\n", timestamp, message, attrString)
	case LevelWarn:
		fmt.Fprintf(os.Stderr, "[WARN] %s %s%s\n", timestamp, message, attrString)
	case LevelError:
		fmt.Fprintf(os.Stderr, "!!!ERROR!!! %s %s%s\n", timestamp, message, attrString)
	default:
		panic("unreachable")
	}
}

func main() {
	// Create a logger instance
	var logger Logger = &SimpleLogger{}

	ctx := context.Background()

	// Log messages at different levels
	logger.Log(ctx, LevelDebug, "This is a debug message")
	logger.Log(ctx, LevelInfo, "This is an info message")
	logger.Log(ctx, LevelWarn, "This is a warning message", Attr{Key: "id", Value: 42})
	logger.Log(ctx, LevelError, "This is an error message", Attr{Key: "user", Value: "admin"})
}
