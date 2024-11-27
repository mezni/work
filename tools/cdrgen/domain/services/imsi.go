package services

import (
	"errors"
	"math/rand"
	"sync"
	"time"
	"github.com/mezni/bridge/tools/cdrgen/domain/valueobjects"
)

const (
	MCCLength   = 3
	MNCLength   = 3
	IMSILength  = 15
)

var (
	ErrInvalidMCCMNC                 = errors.New("invalid MCC or MNC: must be exactly 3 numeric characters each")
	ErrInvalidSubscriberNumberLength = errors.New("subscriber number length must match remaining digits for a valid IMSI")
)

type IMSIGenerator struct {
	randSource *rand.Rand
	mu         sync.Mutex
}

func NewIMSIGenerator() *IMSIGenerator {
	return &IMSIGenerator{
		randSource: rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

func (g *IMSIGenerator) GenerateIMSI(mcc, mnc string, subscriberNumberLength int) (valueobjects.IMSI, error) {
	if len(mcc) != MCCLength || len(mnc) != MNCLength {
		return valueobjects.IMSI{}, ErrInvalidMCCMNC
	}

	remainingLength := IMSILength - len(mcc) - len(mnc)
	if subscriberNumberLength != remainingLength {
		return valueobjects.IMSI{}, ErrInvalidSubscriberNumberLength
	}

	subscriberNumber := g.generateSubscriberNumber(subscriberNumberLength)
	imsiValue := mcc + mnc + subscriberNumber

	return valueobjects.NewIMSI(imsiValue)
}

func (g *IMSIGenerator) generateSubscriberNumber(length int) string {
	g.mu.Lock()
	defer g.mu.Unlock()

	digits := make([]byte, length)
	for i := 0; i < length; i++ {
		digits[i] = byte('0' + g.randSource.Intn(10))
	}
	return string(digits)
}
