package msisdn

import (
	"fmt"
	"math/rand"
)

// generateRandomNumber generates a random number with a specified number of digits.
func generateRandomNumber(digits ...int) (string, error) {
	// Set default digits to 6 if not provided
	digitCount := 6
	if len(digits) > 0 && digits[0] >= 0 {
		digitCount = digits[0]
	}
	randomNumber := ""
	for i := 0; i < digitCount; i++ {
		randomNumber += fmt.Sprintf("%d", rand.Intn(10))
	}
	return randomNumber, nil
}

// generateRandomNumber generates a random msisdn.
func generateMSISDN(prefixes []string, digits int, local ...bool) (string, error) {
	localFlag := false
	if len(local) > 0 {
		localFlag = local[0]
	}
	msisdn := ""
	msisdn += prefixes[rand.Intn(len(prefixes))]

	randomNumber, err := generateRandomNumber(digits)
	if err != nil {
		return "", err
	}
	msisdn += randomNumber

	if !localFlag {
		msisdn = "+" + msisdn
	}
	return msisdn, nil
}