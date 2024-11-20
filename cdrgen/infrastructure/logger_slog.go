package infrastructure


import (
	"log/slog"
)

type slogLogger struct {
	logger *slog.Logger
}

func NewSlogLogger(group *slog.Logger) Logger {
	return &slogLogger{logger: group}
}

func (l *slogLogger) Debug(msg string, fields ...slog.Attr) {
	l.logger.Debug(msg, fields...)
}

func (l *slogLogger) Info(msg string, fields ...slog.Attr) {
	l.logger.Info(msg, fields...)
}

func (l *slogLogger) Warn(msg string, fields ...slog.Attr) {
	l.logger.Warning(msg, fields...)
}

func (l *slogLogger) Error(msg string, fields ...slog.Attr) {
	l.logger.Error(msg, fields...)
}

func (l *slogLogger) Fatal(msg string, fields ...slog.Attr) {
	l.logger.Fatal(msg, fields...)
}