package logging

import "context"

type Logger interface {
	Info(ctx context.Context, message string, keysAndValues ...any)
	Error(ctx context.Context, message string, keysAndValues ...any)
	Debug(ctx context.Context, message string, keysAndValues ...any)
	Warn(ctx context.Context, message string, keysAndValues ...any)
}
