package main

import (
	"context"
	"fmt"
	"github.com/mezni/bridge/tools/cdrgen/application"
	"github.com/mezni/bridge/tools/cdrgen/infrastructure/logging"
)

func main() {
	// Create a new logger instance
	logger := logging.NewSlogLogger("IMSI")

	// Create a context, optionally with values
	ctx := context.Background()
	ctx = context.WithValue(ctx, "requestID", "12345") // Adding requestID to the context

	// Debugging: Print requestID to confirm it's set in context
	fmt.Println("requestID in context before calling GenerateAndUseIMSI:", ctx.Value("requestID"))

	// Call the function that generates and uses an IMSI, passing the logger and context
	application.GenerateAndUseIMSI(ctx, logger)
}
