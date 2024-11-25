package logger

// Logger interface now only requires the message and optional arguments.
type Logger interface {
	// Log records a log message
	Log(msg string, args ...any) error

	// Info logs an info level message
	Info(msg string, args ...any) error

	// Error logs an error level message
	Error(msg string, args ...any) error

	// Debug logs a debug level message
	Debug(msg string, args ...any) error
}