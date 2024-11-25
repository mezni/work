package main

import (
	"fmt"
	"math/rand"
	"time"
)

// MSISDNConfig holds the input values for country code, operator prefixes, and number format
type MSISDNConfig struct {
	CountryCode     string   // Country code for the phone number
	OperatorPrefixes []string // List of operator prefixes
	NumberFormat    string   // Format for the subscriber number (e.g., %07d)
}

// GenerateRandomMSISDN generates a random MSISDN based on the MSISDNConfig struct
func GenerateRandomMSISDN(config MSISDNConfig) string {
	// Randomly pick an operator prefix
	rand.Seed(time.Now().UnixNano())
	prefix := config.OperatorPrefixes[rand.Intn(len(config.OperatorPrefixes))]

	// Generate a subscriber number based on the given format
	subscriberNumber := fmt.Sprintf(config.NumberFormat, rand.Intn(10000000))

	// Combine the country code, operator prefix, and subscriber number
	msisdn := fmt.Sprintf("%s%s%s", config.CountryCode, prefix, subscriberNumber)

	return msisdn
}

func main() {
	// Define the MSISDNConfig struct with input values
	config := MSISDNConfig{
		CountryCode:     "+216",                     // Country code for Tunisia
		OperatorPrefixes: []string{"22", "23", "24", "25", "26", "27", "28", "29"}, // Operator prefixes
		NumberFormat:    "%07d",                     // Format for the subscriber number (7 digits)
	}

	// Generate and print a random MSISDN
	msisdn := GenerateRandomMSISDN(config)
	fmt.Println("Random Tunisian MSISDN:", msisdn)
}
