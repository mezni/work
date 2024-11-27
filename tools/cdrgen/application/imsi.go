package application

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/infrastructure/logging"
	"github.com/mezni/bridge/tools/cdrgen/domain/services"
)

func GenerateAndUseIMSI(ctx context.Context, logger logging.Logger) {
	// Initialize the IMSI generator
	generator := services.NewIMSIGenerator()

	// Example MCC and MNC
	mcc := "310"  // USA
	mnc := "260"  // T-Mobile
	subscriberNumberLength := 9 // Length for the random subscriber number

	// Generate the IMSI
	imsi, err := generator.GenerateIMSI(mcc, mnc, subscriberNumberLength)
	if err != nil {
		// Log the error
		logger.Error(ctx, "Error generating IMSI", "error", err)
		return
	}

	// Log the generated IMSI
	logger.Info(ctx, "Generated IMSI", "imsi", imsi.String())
}
