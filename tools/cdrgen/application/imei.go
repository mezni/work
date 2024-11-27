package application

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/infrastructure/logging"
	"github.com/mezni/bridge/tools/cdrgen/domain/services"
)

func GenerateAndUseIMEI(ctx context.Context, logger logging.Logger) {
	// Initialize the IMEI generator
	generator := services.NewIMEIGenerator()

	// Example TAC (Type Allocation Code)
	tac := "12345678" // Sample TAC for a specific device

	// Example serial number length (must be 6 digits)
	serialNumberLength := 6

	// Generate the IMEI
	imei, err := generator.GenerateIMEI(tac, serialNumberLength)
	if err != nil {
		// Log the error
		logger.Error(ctx, "Error generating IMEI", "error", err)
		return
	}

	// Log the generated IMEI
	logger.Info(ctx, "Generated IMEI", "imei", imei)
}
