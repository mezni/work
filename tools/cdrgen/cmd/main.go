package main

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/application"
	"github.com/mezni/bridge/tools/cdrgen/infrastructure/logging"
)

func main() {
	// Create a new logger instance
	logger := logging.NewSlogLogger("CdrGen")

	// Create a context, optionally with values
	ctx := context.Background()
	ctx = context.WithValue(ctx, "requestID", "12345") // Adding requestID to the context


	// Call the function that generates and uses an IMSI, passing the logger and context
	application.GenerateAndUseIMSI(ctx, logger)
	application.GenerateAndUseIMEI(ctx, logger)
}
