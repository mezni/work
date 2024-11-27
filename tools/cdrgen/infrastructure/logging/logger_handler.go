package logging

import (
	"context"
	"fmt"
	"log/slog"
	"os"
	"time"
)

type CustomHandler struct {
	module string
}

func NewCustomHandler(module string) *CustomHandler {
	return &CustomHandler{module: module}
}

func (h *CustomHandler) Handle(ctx context.Context, r slog.Record) error {
	// Format the log line using the attributes already passed (no need to manually add requestID)
	var logMsg string
	r.Attrs(func(a slog.Attr) bool {
		logMsg += fmt.Sprintf("%s=%v ", a.Key, a.Value)
		return true
	})

	// Format the log line
	logLine := fmt.Sprintf("[%s] [%s] [%s] %s %s\n",
		time.Now().Format(time.RFC3339),
		h.module,
		r.Level.String(),
		r.Message,
		logMsg, // Include all attributes, including requestID, automatically
	)

	_, err := os.Stdout.WriteString(logLine)
	return err
}

func (h *CustomHandler) Enabled(ctx context.Context, level slog.Level) bool {
	return true
}

func (h *CustomHandler) WithAttrs(attrs []slog.Attr) slog.Handler {
	return h
}

func (h *CustomHandler) WithGroup(name string) slog.Handler {
	return h
}
