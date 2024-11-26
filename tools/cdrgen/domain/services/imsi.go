package services

import (
	"errors"
	"fmt"
	"math/rand"
	"time"
	"github.com/mezni/bridge/tools/cdrgen/domain/valueobjects" 
)

var (
	ErrInvalidMCCMNC                = errors.New("MCC and MNC must be 3 digits")
	ErrInvalidSubscriberNumberLength = errors.New("subscriber number length must be greater than zero")
)

type IMSIGenerator struct{}

// NewIMSIGenerator creates a new IMSI generator instance
func NewIMSIGenerator() *IMSIGenerator {
	return &IMSIGenerator{}
}

// GenerateIMSI generates an IMSI based on MCC, MNC, and a random subscriber number of a given length
func (g *IMSIGenerator) GenerateIMSI(mcc string, mnc string, subscriberNumberLength int) (valueobjects.IMSI, error) {
	// Validate MCC and MNC (must be 3 digits)
	if len(mcc) != 3 || len(mnc) != 3 {
		return valueobjects.IMSI{}, ErrInvalidMCCMNC
	}

	// Validate the subscriber number length (should be a positive number)
	if subscriberNumberLength <= 0 {
		return valueobjects.IMSI{}, ErrInvalidSubscriberNumberLength
	}

	// Generate a random subscriber number with the specified length
	subscriberNumber := generateSubscriberNumber(subscriberNumberLength)

	// Construct IMSI (MCC + MNC + Subscriber Number)
	imsiValue := mcc + mnc + subscriberNumber
	return valueobjects.NewIMSI(imsiValue)
}

// generateSubscriberNumber generates a random subscriber number of a given length
func generateSubscriberNumber(length int) string {
	// Using rand.Intn directly without re-seeding each time
	subscriberNumber := fmt.Sprintf("%0"+fmt.Sprintf("%d", length)+"d", rand.Intn(intPow(10, length)))

	// Ensure the length is correct (pad with leading zeros if necessary)
	return subscriberNumber
}

// intPow calculates power of 10 (used to generate random numbers of the given length)
func intPow(base, exp int) int {
	result := 1
	for i := 0; i < exp; i++ {
		result *= base
	}
	return result
}

// Ensure random seed is set once at the start of the program (in main or init).
func init() {
	// This ensures rand is seeded once, at program start
	rand.Seed(time.Now().UnixNano())
}
