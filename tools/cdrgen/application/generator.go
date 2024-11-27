package application

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/domain/services"
	"github.com/mezni/bridge/tools/cdrgen/infrastructure/logging"
)

func GenerateIMSI(ctx context.Context, logger logging.Logger) {
	generator := services.NewIMSIGenerator()

	mcc := "310"
	mnc := "260"
	subscriberNumberLength := 9

	imsi, err := generator.GenerateIMSI(mcc, mnc, subscriberNumberLength)
	if err != nil {
		logger.Error(ctx, "Failed to generate IMSI", "error", err)
		return
	}

	logger.Info(ctx, "Generated IMSI", "imsi", imsi.String())
}

func GenerateIMEI(ctx context.Context, logger logging.Logger) {
	generator := services.NewIMEIGenerator()

	tac := "49015420"
	serialNumberLength := 6

	imei, err := generator.GenerateIMEI(tac, serialNumberLength)
	if err != nil {
		logger.Error(ctx, "Failed to generate IMEI", "error", err)
		return
	}

	logger.Info(ctx, "Generated IMEI", "imei", imei.String())
}


func GenerateMSISDN(ctx context.Context, logger logging.Logger) {
	generator := services.NewMSISDNGenerator()

	countryCode := "216"    // US country code
	networkCode := "55"  // Example network code
	subscriberNumberLength := 6

	msisdn, err := generator.GenerateMSISDN(countryCode, networkCode, subscriberNumberLength)
	if err != nil {
		logger.Error(ctx, "Failed to generate MSISDN", "error", err)
		return
	}

	logger.Info(ctx, "Generated MSISDN", "msisdn", msisdn.String())
}