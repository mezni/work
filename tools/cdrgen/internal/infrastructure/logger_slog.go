package infrastructure

import (
	"fmt"
	"log"
	"os"
	"time"
)

// Logger defines the methods required for a custom logger.
type Logger interface {
	Info(msg string, args ...interface{})
	Error(msg string, args ...interface{})
	Debug(msg string, args ...interface{})
}

// CustomLogger is an implementation of the Logger interface.
type CustomLogger struct {
	module string
	logger *log.Logger
}

// NewCustomLogger creates a new CustomLogger instance.
func NewCustomLogger(module string) *CustomLogger {
	// Initialize a new logger instance with the desired format
	logger := log.New(os.Stdout, "", log.LstdFlags) // Logs to stdout with default timestamp

	return &CustomLogger{
		module: module,
		logger: logger,
	}
}

// Info logs an informational message.
func (l *CustomLogger) Info(msg string, args ...interface{}) {
	l.log("INFO", msg, args...)
}

// Error logs an error message.
func (l *CustomLogger) Error(msg string, args ...interface{}) {
	l.log("ERROR", msg, args...)
}

// Debug logs a debug message.
func (l *CustomLogger) Debug(msg string, args ...interface{}) {
	l.log("DEBUG", msg, args...)
}

// log is a private method to format and log the message with a level.
func (l *CustomLogger) log(level string, msg string, args ...interface{}) {
	// Format the log message with the timestamp and module
	logMessage := fmt.Sprintf("[%s] [%s] [%s] %s", time.Now().Format("2006-01-02 15:04:05"), l.module, level, fmt.Sprintf(msg, args...))

	// Print the formatted log message
	l.logger.Println(logMessage)
}
