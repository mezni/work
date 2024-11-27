package services

import (
	"errors"
	"github.com/mezni/bridge/tools/cdrgen/domain/valueobjects"
)

const (
	IMSILength = 15
	MCCLength  = 3
	MNCLength  = 3
)

var (
	ErrInvalidMCCMNC                 = errors.New("invalid MCC or MNC: must be exactly 3 numeric characters each")
	ErrInvalidSubscriberNumberLength = errors.New("subscriber number length must match remaining digits for a valid IMSI")
)

type IMSIGenerator struct {
	randomGenerator *RandomGenerator
}

func NewIMSIGenerator() *IMSIGenerator {
	return &IMSIGenerator{randomGenerator: NewRandomGenerator()}
}

func (g *IMSIGenerator) GenerateIMSI(mcc, mnc string, subscriberNumberLength int) (valueobjects.IMSI, error) {
	if len(mcc) != MCCLength || len(mnc) != MNCLength {
		return valueobjects.IMSI{}, ErrInvalidMCCMNC
	}

	if len(mcc)+len(mnc)+subscriberNumberLength != IMSILength {
		return valueobjects.IMSI{}, ErrInvalidSubscriberNumberLength
	}

	subscriberNumber := g.randomGenerator.GenerateRandomDigits(subscriberNumberLength)
	imsiValue := mcc + mnc + subscriberNumber

	return valueobjects.NewIMSI(imsiValue)
}
