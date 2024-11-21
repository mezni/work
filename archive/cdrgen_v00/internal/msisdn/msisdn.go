package msisdn

import (
	"fmt"
	"math/rand"
	"time"
)

// MSISDNConfig defines the configuration for generating MSISDN numbers
type MSISDNConfig struct {
	prefixes []string
	digits   int
	local    bool
	rand     *rand.Rand
}

// NewMSISDNConfig initializes a new MSISDNConfig with the specified prefixes, digits, and optional local flag
func NewMSISDNConfig(prefixes []string, digits ...int) *MSISDNConfig {
	digitCount := 6 // Default to 6 digits
	if len(digits) > 0 && digits[0] > 0 {
		digitCount = digits[0]
	}

	return &MSISDNConfig{
		prefixes: prefixes,
		digits:   digitCount,
		local:    false,
		rand:     rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

// SetLocal sets the local flag
func (m *MSISDNConfig) SetLocal(local bool) *MSISDNConfig {
	m.local = local
	return m
}

// generateRandomNumber generates a random number with a specified number of digits.
func generateRandomNumber(digits ...int) string {
	// Set default digits to 6 if not provided
	digitCount := 6
	if len(digits) > 0 && digits[0] >= 0 {
		digitCount = digits[0]
	}
	randomNumber := ""
	for i := 0; i < digitCount; i++ {
		randomNumber += fmt.Sprintf("%d", rand.Intn(10))
	}
	return randomNumber
}

func (m *MSISDNConfig) Generate() string {
	prefixes := m.prefixes
	digits := m.digits
	local := m.local
	msisdn := ""
	msisdn += prefixes[rand.Intn(len(prefixes))]

	randomNumber := generateRandomNumber(digits)

	msisdn += randomNumber

	if !local {
		msisdn = "+" + msisdn
	}
	return msisdn
}

// GenerateList generates a list of MSISDNs
func (m *MSISDNConfig) GenerateList(n int) []string {
	var msisdns []string
	for i := 0; i < n; i++ {
		msisdns = append(msisdns, m.Generate())
	}
	return msisdns
}
