package main

import (
	"fmt"
	"math/rand"
	"strconv"
	"strings"

	"gopkg.in/yaml.v3"
)

// MSISDNConfig represents the configuration for generating MSISDNs
type MSISDNConfig struct {
	CountryCode interface{} `yaml:"country_code"`
	NetworkCode []string    `yaml:"network_code"`
	Format      string      `yaml:"format"`
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
  - name: calling_party_number
    type: msisdn
    msisdn:
      country_code: 216
      network_code: [50-55,30-35]
      format: '+%country_code%%network_code%'
  - name: called_party_number
    type: msisdn
    msisdn:
      country_code: [216,212]
      network_code: [50-55,30-35]
      format: '+%country_code%%network_code%'
`

	// Unmarshal YAML configuration
	var config Config
	err := yaml.Unmarshal([]byte(yamlConfig), &config)
	if err != nil {
		fmt.Println(err)
		return
	}

	// Generate MSISDNs for each column
	for _, column := range config.Columns {
		msisdn := generateMSISDN(column.MSISDN)
		fmt.Printf("%s: %s\n", column.Name, msisdn)
	}
}

func generateMSISDN(config MSISDNConfig) string {
	var countryCode string
	var networkCode string

	// Check if country_code is a slice or a single value
	switch cc := config.CountryCode.(type) {
	case []interface{}:
		// Select a random country code from the slice
		countryCode = fmt.Sprintf("%v", cc[rand.Intn(len(cc))])
	case int:
		// Convert the single country code to a string
		countryCode = fmt.Sprintf("%v", cc)
	default:
		fmt.Println("Unsupported country_code type")
		return ""
	}

	// Select a random network code range
	networkCodeRange := config.NetworkCode[rand.Intn(len(config.NetworkCode))]

	// Extract the start and end of the network code range
	parts := strings.Split(networkCodeRange, "-")
	start, _ := strconv.Atoi(parts[0])
	end, _ := strconv.Atoi(parts[1])

	// Generate a random network code within the selected range
	networkCode = fmt.Sprintf("%d", rand.Intn(end-start+1)+start)

	// Replace placeholders in the format string with actual values
	msisdn := config.Format
	msisdn = replacePlaceholder(msisdn, "%country_code%", countryCode)
	msisdn = replacePlaceholder(msisdn, "%network_code%", networkCode)

	return msisdn
}

func replacePlaceholder(str, placeholder, value string) string {
	return strings.Replace(str, placeholder, value, 1)
}
