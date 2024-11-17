package main

import (
	"fmt"
	"math/rand"

	"gopkg.in/yaml.v3"
)

const (
	DEFAULT_COUNTRY_CODE_KEY = "216"
)

// MSISDNConfig represents the configuration for generating MSISDNs
type MSISDNConfig struct {
	CountryCode interface{} `yaml:"country_code"`
	// NetworkCode interface{} `yaml:"network_code"`
	// Format      string      `yaml:"format"`
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
      format: '+%country_code% %network_code%'
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

func generateMSISDN(config MSISDNConfig) string {
	var countryCode string

	// Check if country_code is a slice or a single value
	switch cc := config.CountryCode.(type) {
	case []interface{}:
		// Select a random country code from the slice
		countryCode = fmt.Sprintf("%v", cc[rand.Intn(len(cc))])
	case int:
		// Convert the single country code to a string
		countryCode = fmt.Sprintf("%v", cc)
	default:
		return DEFAULT_COUNTRY_CODE_KEY
	}
	msisdn := countryCode

	return msisdn
}