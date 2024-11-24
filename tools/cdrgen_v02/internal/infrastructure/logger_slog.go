package infrastructure

import (
	"context"
	"fmt"
	"log/slog"
//"github.com/mezni/bridge/tools/cdrgen/internal/application"
	"time"
)

// SlogLogger implements the application.Logger interface using the slog package
type SlogLogger struct {
	ctx    context.Context
	module string
	logger *slog.Logger
}

// NewSlogLogger creates a new instance of SlogLogger
func NewSlogLogger() *SlogLogger {
	handler := slog.NewTextHandler(slog.NewTextHandlerConfig{
		TimeFormat: "2006-01-02 15:04:05", // Timestamp format
	})

	logger := slog.New(handler)
	return &SlogLogger{logger: logger}
}

// Init initializes the logger with context and module, retaining them for future log calls
func (l *SlogLogger) Init(ctx context.Context, module string) Logger {
	l.ctx = ctx
	l.module = module
	return l
}

// Info logs an info-level message with the retained context and module
func (l *SlogLogger) Info(msg string, args ...interface{}) {
	l.log("INFO", msg, args...)
}

// Error logs an error-level message with the retained context and module
func (l *SlogLogger) Error(msg string, args ...interface{}) {
	l.log("ERROR", msg, args...)
}

// Debug logs a debug-level message with the retained context and module
func (l *SlogLogger) Debug(msg string, args ...interface{}) {
	l.log("DEBUG", msg, args...)
}

// log formats the log output in the desired format: [timestamp] [Module] [level] message
func (l *SlogLogger) log(level, msg string, args ...interface{}) {
	timestamp := time.Now().Format("2006-01-02 15:04:05")

	// Format args into key=value pairs if provided
	argsString := formatArgs(args)

	// Output the log message in the required format
	fmt.Printf("[%s] [%s] [%s] %s%s\n", timestamp, l.module, level, msg, argsString)
}

// formatArgs formats key-value pairs for structured logging
func formatArgs(args []interface{}) string {
	if len(args) == 0 {
		return ""
	}
	parts := []string{}
	for i := 0; i < len(args); i += 2 {
		if i+1 < len(args) {
			parts = append(parts, fmt.Sprintf("%v=%v", args[i], args[i+1]))
		} else {
			parts = append(parts, fmt.Sprintf("%v=<missing>", args[i]))
		}
	}
	return " " + fmt.Sprint(parts)
}
