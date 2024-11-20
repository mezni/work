package logger

import (
	"log/slog"
	"os"
)

// Logger wraps slog.Logger to provide structured logging capabilities.
type Logger struct {
	logger *slog.Logger
}

// NewLogger initializes and returns a new Logger instance.
// Parameters:
//   - output: "stdout" for console logging or a file path for file logging.
//   - level: the minimum log level (e.g., slog.LevelInfo, slog.LevelDebug).
func NewLogger(output string, level slog.Level) (*Logger, error) {
	var handler slog.Handler
	var err error

	if output == "stdout" {
		// Configure logging to stdout
		handler = slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{
			Level: level,
		})
	} else {
		// Configure logging to a file
		file, err := os.OpenFile(output, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			return nil, err
		}
		handler = slog.NewTextHandler(file, &slog.HandlerOptions{
			Level: level,
		})
	}

	return &Logger{
		logger: slog.New(handler),
	}, err
}

// Info logs informational messages with optional key-value pairs.
func (l *Logger) Info(msg string, keysAndValues ...any) {
	l.logger.Info(msg, keysAndValues...)
}

// Debug logs debug messages with optional key-value pairs.
func (l *Logger) Debug(msg string, keysAndValues ...any) {
	l.logger.Debug(msg, keysAndValues...)
}

// Error logs error messages with optional key-value pairs.
func (l *Logger) Error(msg string, keysAndValues ...any) {
	l.logger.Error(msg, keysAndValues...)
}


/*
func main() {
	// Example 1: Log to stdout with Debug level
	logStdout, err := logger.NewLogger("stdout", slog.LevelDebug)
	if err != nil {
		panic(err)
	}
	logStdout.Info("Logging to stdout", "component", "main")
	logStdout.Debug("Debug message", "key", "value")

	// Example 2: Log to a file with Info level
	logFile, err := logger.NewLogger("app.log", slog.LevelInfo)
	if err != nil {
		panic(err)
	}
	logFile.Info("Logging to file", "component", "main")
	logFile.Debug("This debug message will not be logged", "key", "value") // Below LevelInfo
}

*/