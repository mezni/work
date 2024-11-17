package main

import (
	"fmt"
	"math/rand"
	"time"

	"gopkg.in/yaml.v3"
)

const (
	defaultCountryCode = "216"
)

// MSISDNConfig represents the configuration for generating MSISDNs
type MSISDNConfig struct {
	CountryCode interface{} `yaml:"country_code"`
}

// ColumnConfig represents the configuration for a column
type ColumnConfig struct {
	Name   string       `yaml:"name"`
	Type   string       `yaml:"type"`
	MSISDN MSISDNConfig `yaml:"msisdn"`
}

// Config represents the YAML configuration
type Config struct {
	Columns []ColumnConfig `yaml:"columns"`
}

func main() {
	// Initialize random number generator
	rand.Seed(time.Now().UnixNano())

	// Sample YAML configuration
	yamlConfig := `
columns:
  - name: calling_party_number1
    type: msisdn
  - name: calling_party_number
    type: msisdn
    msisdn:
      country_code: 216
  - name: called_party_number
    type: msisdn
    msisdn:
      country_code: [216,212]
`

	// Unmarshal YAML configuration
	var config Config
	err := yaml.Unmarshal([]byte(yamlConfig), &config)
	if err != nil {
		fmt.Println(err)
		return
	}

	for _, column := range config.Columns {
		msisdn := generateMSISDN(column.MSISDN)
		fmt.Println(msisdn)
	}
}

func generateMSISDN(config MSISDNConfig) []string {
	var countryCodes []string

	// Check if country_code is a slice or a single value
	switch cc := config.CountryCode.(type) {
	case []interface{}:
		// Convert the slice of country codes to a slice of strings
		for _, code := range cc {
			countryCodes = append(countryCodes, fmt.Sprintf("%v", code))
		}
	case string:
		// Add the country code to the slice
		countryCodes = append(countryCodes, cc)
	case int:
		// Convert the single country code to a string and add it to the slice
		countryCodes = append(countryCodes, fmt.Sprintf("%v", cc))
	default:
		// Return a slice with the default country code if type is unknown
		return []string{defaultCountryCode}
	}

	return countryCodes
}
