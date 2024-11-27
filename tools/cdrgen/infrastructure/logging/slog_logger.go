package logging

import (
	"context"
	"log/slog"
)


type SlogLogger struct {
	logger *slog.Logger
}

func NewSlogLogger(module string) *SlogLogger {
	handler := NewCustomHandler(module)
	logger := slog.New(handler)
	return &SlogLogger{logger: logger}
}

func (l *SlogLogger) Info(ctx context.Context, msg string, args ...any) {
	// Add requestID from context into the log entry
	requestID, _ := ctx.Value("requestID").(string)
	args = append(args, "requestID", requestID)
	l.logger.Info(msg, args...)
}

func (l *SlogLogger) Error(ctx context.Context, msg string, args ...any) {
	// Add requestID from context into the log entry
	requestID, _ := ctx.Value("requestID").(string)
	args = append(args, "requestID", requestID)
	l.logger.Error(msg, args...)
}

func (l *SlogLogger) Debug(ctx context.Context, msg string, args ...any) {
	// Add requestID from context into the log entry
	requestID, _ := ctx.Value("requestID").(string)
	args = append(args, "requestID", requestID)
	l.logger.Debug(msg, args...)
}

func (l *SlogLogger) Warn(ctx context.Context, msg string, args ...any) {
	// Add requestID from context into the log entry
	requestID, _ := ctx.Value("requestID").(string)
	args = append(args, "requestID", requestID)
	l.logger.Warn(msg, args...)
}
