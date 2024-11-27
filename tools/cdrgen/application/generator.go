package application

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/domain/services"
	"github.com/mezni/bridge/tools/cdrgen/infrastructure/logging"
	"time"
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

	countryCode := "216" // US country code
	networkCode := "55"  // Example network code
	subscriberNumberLength := 6

	msisdn, err := generator.GenerateMSISDN(countryCode, networkCode, subscriberNumberLength)
	if err != nil {
		logger.Error(ctx, "Failed to generate MSISDN", "error", err)
		return
	}

	logger.Info(ctx, "Generated MSISDN", "msisdn", msisdn.String())
}

func GenerateIP(ctx context.Context, logger logging.Logger) {
	generator := services.NewIPGenerator()

	ipVersion := services.IPv4
	ipType := services.Public

	ip, err := generator.GenerateIP(ipVersion, ipType)
	if err != nil {
		logger.Error(ctx, "Failed to generate IP address", "error", err)
		return
	}

	logger.Info(ctx, "Generated IP address", "ip", ip)
}

func GenerateDatetime(ctx context.Context, logger logging.Logger) {
	generator := services.NewDatetimeGenerator()

	// Specify the datetime range
	start := time.Date(2020, 1, 1, 0, 0, 0, 0, time.UTC)
	end := time.Date(2023, 12, 31, 23, 59, 59, 0, time.UTC)

	// Generate random datetime
	datetime, err := generator.GenerateRandomDatetime(start, end)
	if err != nil {
		logger.Error(ctx, "Failed to generate random datetime", "error", err)
		return
	}

	// Format the datetime to a readable string
	formattedDatetime := generator.FormatDatetime(datetime, time.RFC1123, nil)

	logger.Info(ctx, "Generated Datetime", "datetime", formattedDatetime)
}
