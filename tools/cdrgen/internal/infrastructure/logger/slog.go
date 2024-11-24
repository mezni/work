package logger

import (
	"context"
	"fmt"
	"log/slog"
	"time"
)

// CustomContextKey is a custom type for context keys to avoid collisions
type CustomContextKey string

// Define custom log levels (map to slog levels internally)
type LogLevel int

const (
	DebugLevel LogLevel = iota
	InfoLevel
	ErrorLevel
)

// SlogLogger struct holds the log level, module name, and context
type SlogLogger struct {
	level  LogLevel
	module string
	ctx    context.Context
}

// NewSlogLogger initializes a new logger with a predefined log level, module, and optional context
func NewSlogLogger(level LogLevel, module string, ctx ...context.Context) *SlogLogger {
	var finalCtx context.Context
	if len(ctx) > 0 {
		finalCtx = ctx[0]
	} else {
		finalCtx = context.Background()
	}

	return &SlogLogger{
		level:  level,
		module: module,
		ctx:    finalCtx,
	}
}

// logLevelToSlogLevel maps custom log levels to slog levels
func (l *SlogLogger) logLevelToSlogLevel() slog.Level {
	switch l.level {
	case DebugLevel:
		return slog.LevelDebug
	case InfoLevel:
		return slog.LevelInfo
	case ErrorLevel:
		return slog.LevelError
	default:
		return slog.LevelInfo
	}
}

// Log method handles logging messages with the pre-defined level, module, and context
func (l *SlogLogger) Log(msg string, args ...any) error {
	// Format context information if it exists
	contextInfo := ""
	if l.ctx != nil {
		contextValue := l.ctx.Value("context")
		if contextValue != nil {
			contextData, ok := contextValue.(map[any]any)
			if ok {
				contextInfo = "Context=["
				for k, v := range contextData {
					contextInfo += fmt.Sprintf("%s:%v", k, v)
					if k != nil {
						contextInfo += " "
					}
				}
				contextInfo += "]"
			} else {
				contextInfo = "Context=[invalid type in context]"
			}
		}
	}

	// Format args as key=value in the format Args=[key1=value1, key2=value2]
	argsInfo := ""
	if len(args) > 0 {
		argsInfo += "Args=["
		for i := 0; i < len(args); i += 2 {
			if i+1 < len(args) {
				argsInfo += fmt.Sprintf("%s=%v", args[i], args[i+1])
				if i+2 < len(args) {
					argsInfo += ", "
				}
			}
		}
		argsInfo += "]"
	}

	// Timestamp and module are included in the log
	timestamp := time.Now().Format(time.RFC3339)
	if len(args) > 0 {
		if contextInfo != "" {
			fmt.Printf("[%s] [%s] [%s] %s - %s %s\n", timestamp, l.module, l.logLevelToSlogLevel(), msg, contextInfo, argsInfo)
		} else {
			fmt.Printf("[%s] [%s] [%s] %s - %s\n", timestamp, l.module, l.logLevelToSlogLevel(), msg, argsInfo)
		}
	} else {
		if contextInfo != "" {
			fmt.Printf("[%s] [%s] [%s] %s %s\n", timestamp, l.module, l.logLevelToSlogLevel(), msg, contextInfo)
		} else {
			fmt.Printf("[%s] [%s] [%s] %s\n", timestamp, l.module, l.logLevelToSlogLevel(), msg)
		}
	}
	return nil
}

// Info logs an info level message
func (l *SlogLogger) Info(msg string, args ...any) error {
	l.level = InfoLevel
	return l.Log(msg, args...)
}

// Error logs an error level message
func (l *SlogLogger) Error(msg string, args ...any) error {
	l.level = ErrorLevel
	return l.Log(msg, args...)
}

// Debug logs a debug level message
func (l *SlogLogger) Debug(msg string, args ...any) error {
	l.level = DebugLevel
	return l.Log(msg, args...)
}
