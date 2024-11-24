package logging

import (
	"fmt"
	"golang.org/x/exp/slog"
	"time"
)

// SlogLogger is an implementation of the Logger interface using Go's slog package.
type SlogLogger struct {
	logger *slog.Logger
}

// NewSlogLogger creates a new SlogLogger instance.
func NewSlogLogger(module string) *SlogLogger {
	// Create a custom handler with the given module name
	handler := NewCustomHandler(module)

	// Initialize a new slog logger with the custom handler
	return &SlogLogger{
		logger: slog.New(handler),
	}
}

// Info logs an informational message.
func (l *SlogLogger) Info(msg string, args ...interface{}) {
	l.logger.Info(msg, args...)
}

// Error logs an error message.
func (l *SlogLogger) Error(msg string, args ...interface{}) {
	l.logger.Error(msg, args...)
}

// Debug logs a debug message.
func (l *SlogLogger) Debug(msg string, args ...interface{}) {
	l.logger.Debug(msg, args...)
}

// CustomHandler is a custom log handler that formats logs with timestamp, module, level, and message.
type CustomHandler struct {
	Handler slog.Handler
	Module  string
}

// NewCustomHandler creates a new CustomHandler instance.
func NewCustomHandler(module string) *CustomHandler {
	return &CustomHandler{
		Handler: slog.NewTextHandler(slog.LevelInfo), // Default handler with info level
		Module:  module,
	}
}

// Handle implements the slog.Handler interface.
// This method formats the log entries to the desired format.
func (h *CustomHandler) Handle(r slog.Record) error {
	// Get the timestamp formatted as [YYYY-MM-DD HH:MM:SS]
	timestamp := time.Now().Format("2006-01-02 15:04:05")

	// Log level
	level := r.Level.String()

	// Format the log entry
	logMessage := fmt.Sprintf("[%s] [%s] [%s] %s", timestamp, h.Module, level, r.Message)

	// Log the message using the default handler
	fmt.Println(logMessage)

	return nil
}
