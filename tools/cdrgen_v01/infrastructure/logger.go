package infrastructure

import (
	"fmt"
	"time"
)

// Logger is a simple structured logger that implements the domain.Logger interface.
type Logger struct {
	programName string
}

// NewLogger creates a new instance of Logger.
func NewLogger(programName string) *Logger {
	return &Logger{programName: programName}
}

// Info logs an informational message.
func (l *Logger) Info(msg string, args ...any) {
	l.log("INFO", msg, args...)
}

// Error logs an error message.
func (l *Logger) Error(msg string, args ...any) {
	l.log("ERROR", msg, args...)
}

// Debug logs a debug message.
func (l *Logger) Debug(msg string, args ...any) {
	l.log("DEBUG", msg, args...)
}

// Warn logs a warning message.
func (l *Logger) Warn(msg string, args ...any) {
	l.log("WARN", msg, args...)
}

// log formats and outputs the log message.
func (l *Logger) log(level, msg string, args ...any) {
	fmt.Printf("[%s] [%s] [%s] %s\n", time.Now().Format("2006-01-02 15:04:05"), l.programName, level, msg)
}
