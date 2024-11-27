package services

import (
	"errors"
	"github.com/mezni/bridge/tools/cdrgen/domain/valueobjects"
)

const IMEILength = 15

var ErrInvalidTAC = errors.New("invalid TAC: must be 8 numeric characters")

type IMEIGenerator struct {
	randomGenerator *RandomGenerator
}

func NewIMEIGenerator() *IMEIGenerator {
	return &IMEIGenerator{randomGenerator: NewRandomGenerator()}
}

func (g *IMEIGenerator) GenerateIMEI(tac string, serialNumberLength int) (valueobjects.IMEI, error) {
	if len(tac) != 8 {
		return valueobjects.IMEI{}, ErrInvalidTAC
	}

	if len(tac)+serialNumberLength+1 != IMEILength {
		return valueobjects.IMEI{}, ErrInvalidSubscriberNumberLength
	}

	serialNumber := g.randomGenerator.GenerateRandomDigits(serialNumberLength)
	imeiValue := tac + serialNumber + "0" // Placeholder checksum

	return valueobjects.NewIMEI(imeiValue)
}
