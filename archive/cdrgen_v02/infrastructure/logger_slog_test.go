package infrastructure

import (
	"bytes"
	"testing"
	"log/slog"
)

// Helper function to capture log output
func captureLogOutput(logger Logger, level string, message string, keysAndValues ...any) string {
	var buf bytes.Buffer
	handler := slog.NewTextHandler(&buf, nil) // Capture log output into a buffer

	// Set the logger to use the buffer
	slogLogger := logger.(*SlogLogger) // Type assertion to access SlogLogger methods
	slogLogger.logger = slog.New(handler)

	// Log based on the level
	switch level {
	case "info":
		slogLogger.Info(message, keysAndValues...)
	case "error":
		slogLogger.Error(message, keysAndValues...)
	case "debug":
		slogLogger.Debug(message, keysAndValues...)
	}

	return buf.String()
}

// Test that Info logs at InfoLevel or lower
func TestSlogLogger_InfoLevel(t *testing.T) {
	logger := NewSlogLogger()
	logger.SetLevel(InfoLevel)

	message := "Info level message"
	output := captureLogOutput(logger, "info", message)

	if !contains(output, message) {
		t.Errorf("expected log output to contain %q, got %q", message, output)
	}
}

// Test that Debug does not log at InfoLevel
func TestSlogLogger_DebugLevel(t *testing.T) {
	logger := NewSlogLogger()
	logger.SetLevel(InfoLevel)

	message := "Debug level message"
	output := captureLogOutput(logger, "debug", message)

	if contains(output, message) {
		t.Errorf("expected log output to NOT contain %q, got %q", message, output)
	}
}

// Test that Debug logs at DebugLevel
func TestSlogLogger_DebugLevelSet(t *testing.T) {
	logger := NewSlogLogger()
	logger.SetLevel(DebugLevel)

	message := "Debug level message"
	output := captureLogOutput(logger, "debug", message)

	if !contains(output, message) {
		t.Errorf("expected log output to contain %q, got %q", message, output)
	}
}

// Helper function to check if a substring exists in a string
func contains(str, substr string) bool {
	return bytes.Contains([]byte(str), []byte(substr))
}
