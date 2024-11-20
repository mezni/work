package main

import (
	"context"
	"fmt"
	"log/slog"
	"os"
	"time"
)

// Define log levels
const (
	DebugLevel = iota
	InfoLevel
	WarnLevel
	ErrorLevel
)

// Logger interface defines logging methods with levels.
type Logger interface {
	Info(message string, attrs ...Attr)
	Debug(message string, attrs ...Attr)
	Warn(message string, attrs ...Attr)
	Error(message string, attrs ...Attr)
	SetLogLevel(level int)
}

// SlogLogger is an exported struct implementing the Logger interface.
type SlogLogger struct {
	logger    *slog.Logger
	module    string
	logLevel  int // Current log level
	ctx       context.Context // Context to store across log calls
}

// Attr represents a key-value pair for log attributes.
type Attr struct {
	Key   string
	Value any
}

// NewLogger creates a new SlogLogger instance with the specified module name and context.
func NewLogger(module string, logLevel int, ctx context.Context) Logger {
	// Initialize slog with a text handler and options
	handler := slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{})
	return &SlogLogger{
		logger:   slog.New(handler),
		module:   module,
		logLevel: logLevel,
		ctx:      ctx, // Set the context here
	}
}

// Info logs an informational message with optional attributes.
func (l *SlogLogger) Info(message string, attrs ...Attr) {
	if l.logLevel <= InfoLevel {
		l.log("info", message, attrs...)
	}
}

// Debug logs a debug message with optional attributes.
func (l *SlogLogger) Debug(message string, attrs ...Attr) {
	if l.logLevel <= DebugLevel {
		l.log("debug", message, attrs...)
	}
}

// Warn logs a warning message with optional attributes.
func (l *SlogLogger) Warn(message string, attrs ...Attr) {
	if l.logLevel <= WarnLevel {
		l.log("warn", message, attrs...)
	}
}

// Error logs an error message with optional attributes.
func (l *SlogLogger) Error(message string, attrs ...Attr) {
	if l.logLevel <= ErrorLevel {
		l.log("error", message, attrs...)
	}
}

// SetLogLevel sets the log level for the logger.
func (l *SlogLogger) SetLogLevel(level int) {
	l.logLevel = level
}

// log is a helper function for structured logging.
func (l *SlogLogger) log(level, message string, attrs ...Attr) {
	// Get the request_id from the context
	requestID, _ := l.ctx.Value("request_id").(string)

	// Use RFC3339 timestamp format
	timestamp := time.Now().Format(time.RFC3339)

	// Format attributes
	attrString := fmt.Sprintf("request_id=%s", requestID)
	for _, attr := range attrs {
		attrString += fmt.Sprintf(" %s=%v", attr.Key, attr.Value)
	}

	// Print formatted log
	fmt.Fprintf(os.Stderr, "[%s] [%s] [%s] %s %s\n", timestamp, l.module, level, message, attrString)
}

func main() {
	// Create a context with some values
	ctx := context.WithValue(context.Background(), "request_id", "12345")

	// Initialize the logger with a module name, the desired log level (InfoLevel, DebugLevel, etc.), and context
	logger := NewLogger("main", DebugLevel, ctx)

	// Log messages at different levels
	logger.Info("Application started", Attr{Key: "version", Value: "1.0.0"})
	logger.Debug("Debugging mode enabled", Attr{Key: "debug_level", Value: "verbose"})
	logger.Warn("This is a warning", Attr{Key: "warning_code", Value: "123"})
	logger.Error("This is an error", Attr{Key: "error_code", Value: "404"})

	// Changing log level to InfoLevel (this will stop Debug level logs)
	logger.SetLogLevel(InfoLevel)
	logger.Debug("This debug message will not appear", Attr{Key: "level", Value: "debug"})

	// Info, Warn, and Error level logs will still be printed
	logger.Info("Processing completed", Attr{Key: "status", Value: "success"})
	logger.Warn("Low disk space", Attr{Key: "disk", Value: "low"})
	logger.Error("File not found", Attr{Key: "file", Value: "/path/to/file"})

	fmt.Println("Application finished")
}
