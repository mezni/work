
package infrastructure

import (
	"log/slog"
)

type Logger interface {
	Debug(msg string, fields ...slog.Attr)
	Info(msg string, fields ...slog.Attr)
	Warn(msg string, fields ...slog.Attr)
	Error(msg string, fields ...slog.Attr)
	Fatal(msg string, fields ...slog.Attr)
}