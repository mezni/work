package services

import (
	"errors"
	"math/rand"
	"sync"
	"time"
	"strconv"
)

const (
	TACLength   = 8
	SerialNumberLength = 6
	IMEILength = 15
)

var (
	ErrInvalidTAC = errors.New("TAC must be exactly 8 numeric digits")
	ErrInvalidSerialNumberLength = errors.New("serial number length must match remaining digits for a valid IMEI")
)

type IMEIGenerator struct {
	randSource *rand.Rand
	mu         sync.Mutex
}

func NewIMEIGenerator() *IMEIGenerator {
	return &IMEIGenerator{
		randSource: rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

// GenerateIMEI generates the IMEI number
func (g *IMEIGenerator) GenerateIMEI(tac string, serialNumberLength int) (string, error) {
	if len(tac) != TACLength {
		return "", ErrInvalidTAC
	}

	remainingLength := IMEILength - len(tac) - 1 // Minus 1 for the check digit
	if serialNumberLength != remainingLength {
		return "", ErrInvalidSerialNumberLength
	}

	serialNumber := g.generateSerialNumber(serialNumberLength)
	imeiWithoutCheckDigit := tac + serialNumber

	checkDigit := g.calculateCheckDigit(imeiWithoutCheckDigit)
	imei := imeiWithoutCheckDigit + strconv.Itoa(checkDigit)

	return imei, nil
}

// generateSerialNumber generates a random serial number of the given length
func (g *IMEIGenerator) generateSerialNumber(length int) string {
	g.mu.Lock()
	defer g.mu.Unlock()

	digits := make([]byte, length)
	for i := 0; i < length; i++ {
		digits[i] = byte('0' + g.randSource.Intn(10))
	}
	return string(digits)
}

// calculateCheckDigit calculates the Luhn check digit for the IMEI number
func (g *IMEIGenerator) calculateCheckDigit(imei string) int {
	var sum int
	for i, digit := range imei {
		digitInt, _ := strconv.Atoi(string(digit))
		if i%2 == 0 {
			sum += digitInt
		} else {
			doubled := digitInt * 2
			if doubled > 9 {
				sum += doubled - 9
			} else {
				sum += doubled
			}
		}
	}

	checkDigit := (10 - (sum % 10)) % 10
	return checkDigit
}
