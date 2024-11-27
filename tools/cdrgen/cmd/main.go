package main

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/application"
	"github.com/mezni/bridge/tools/cdrgen/infrastructure/logging"
)

func main() {
	// Create a new logger instance
	logger := logging.NewSlogLogger("CdrGen")

	// Create a context with a request ID
	ctx := context.Background()
	ctx = context.WithValue(ctx, "requestID", "12345")

	// Generate IMSI and IMEI using the application layer
	application.GenerateIMSI(ctx, logger)
	application.GenerateIMEI(ctx, logger)
	application.GenerateMSISDN(ctx, logger)
	application.GenerateIP(ctx, logger)
	application.GenerateDatetime(ctx, logger)
}
