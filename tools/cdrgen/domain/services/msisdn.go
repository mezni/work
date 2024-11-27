package services

import (
	"errors"
	"github.com/mezni/bridge/tools/cdrgen/domain/valueobjects"
)

const (
	MSISDNMinLength = 10 // Minimum length of an MSISDN (e.g., 10 digits for U.S.)
	MSISDNMaxLength = 15 // Maximum length of an MSISDN (e.g., international)
)

var (
	ErrInvalidCountryCode  = errors.New("invalid country code: must be 1 to 3 numeric characters")
	ErrInvalidNetworkCode  = errors.New("invalid network code: must be 1 to 4 numeric characters")
	ErrInvalidMSISDNLength = errors.New("invalid MSISDN length: must be between 10 and 15 digits")
)

type MSISDNGenerator struct {
	randomGenerator *RandomGenerator
}

func NewMSISDNGenerator() *MSISDNGenerator {
	return &MSISDNGenerator{randomGenerator: NewRandomGenerator()}
}

func (g *MSISDNGenerator) GenerateMSISDN(countryCode, networkCode string, subscriberNumberLength int) (valueobjects.MSISDN, error) {
	if len(countryCode) < 1 || len(countryCode) > 3 {
		return valueobjects.MSISDN{}, ErrInvalidCountryCode
	}

	if len(networkCode) < 1 || len(networkCode) > 4 {
		return valueobjects.MSISDN{}, ErrInvalidNetworkCode
	}

	totalLength := len(countryCode) + len(networkCode) + subscriberNumberLength
	if totalLength < MSISDNMinLength || totalLength > MSISDNMaxLength {
		return valueobjects.MSISDN{}, ErrInvalidMSISDNLength
	}

	subscriberNumber := g.randomGenerator.GenerateRandomDigits(subscriberNumberLength)
	msisdnValue := countryCode + networkCode + subscriberNumber

	return valueobjects.NewMSISDN(msisdnValue)
}
