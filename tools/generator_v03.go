package main
import (
	"fmt"
	"log"
	"strings"
	"time"

	"gopkg.in/yaml.v3"
	"io/ioutil"
)
type Config struct {
	Outputs []Output `yaml:"outputs"`
}

type Output struct {
	DestinationType string `yaml:"destination_type"`
	Directory       string `yaml:"directory,omitempty"`    // Optional
	FilePattern     string `yaml:"file_pattern,omitempty"` // Optional
	Format          string `yaml:"format,omitempty"`       // Optional
	Delimiter       string `yaml:"delimiter,omitempty"`    // Optional
}


func main() {
	// Read the YAML configuration file
	data, err := ioutil.ReadFile("config.yaml")
	if err != nil {
		log.Fatalf("Error reading YAML file: %v", err)
	}

	// Parse the YAML data
	var config Config
	err = yaml.Unmarshal(data, &config)
	if err != nil {
		log.Fatalf("Error parsing YAML: %v", err)
	}

	// Default values
	defaultDirectory := "."
	defaultFilePattern := "output_{timestamp}.csv"
	defaultFormat := "csv"
	defaultDelimiter := ","

	// Process each output
	for i, output := range config.Outputs {
		// Apply defaults for optional fields
		directory := output.Directory
		if directory == "" {
			directory = defaultDirectory
		}

		filePattern := output.FilePattern
		if filePattern == "" {
			filePattern = defaultFilePattern
		}

		format := output.Format
		if format == "" {
			format = defaultFormat
		}

		delimiter := output.Delimiter
		if delimiter == "" {
			delimiter = defaultDelimiter
		}

		// Generate the file name using the pattern
		timestamp := time.Now().Format("2006-01-02_15-04-05")
		fileName := strings.ReplaceAll(filePattern, "{timestamp}", timestamp)

		// Combine directory and file name into full path
		filePath := fmt.Sprintf("%s/%s", directory, fileName)

		// Print the output configuration
		fmt.Printf("Output #%d:\n", i+1)
		fmt.Printf("  Destination: %s\n", output.DestinationType)
		fmt.Printf("  Directory: %s\n", directory)
		fmt.Printf("  File Name: %s\n", fileName)
		fmt.Printf("  Full Path: %s\n", filePath)
		fmt.Printf("  Format: %s\n", format)
		fmt.Printf("  Delimiter: %s\n\n", delimiter)
	}
}


package main

import (
	"bytes"
	"fmt"
	"log"
	"text/template"

	"gopkg.in/yaml.v3"
	"io/ioutil"
)

type Config struct {
	Variables map[string]interface{} `yaml:"variables"` // General key-value store for variables
	Columns   []Column               `yaml:"columns"`   // List of column definitions
}

type Column struct {
	Name                    string `yaml:"name"`
	Type                    string `yaml:"type"`
	Generator               string `yaml:"generator"`
	Pattern                 string `yaml:"pattern"`
	CountryCodeVariable     string `yaml:"country_code_variable"`
	NetworkCodeVariable     string `yaml:"network_code_variable"`
	SubscriberNumberLength  int    `yaml:"subscriber_number_length"`
}


package main

func main() {
	// Load YAML file
	data, err := ioutil.ReadFile("config.yaml")
	if err != nil {
		log.Fatalf("Error reading YAML file: %v", err)
	}

	// Parse YAML
	var config Config
	err = yaml.Unmarshal(data, &config)
	if err != nil {
		log.Fatalf("Error parsing YAML: %v", err)
	}

	// Process each column
	for _, column := range config.Columns {
		if column.Generator == "msisdn" {
			// Fetch variables for pattern
			countryCode, ok := config.Variables[column.CountryCodeVariable].(int)
			if !ok {
				log.Fatalf("Country code variable '%s' not found or invalid", column.CountryCodeVariable)
			}

			networkCodes, ok := config.Variables[column.NetworkCodeVariable].([]interface{})
			if !ok {
				log.Fatalf("Network codes variable '%s' not found or invalid", column.NetworkCodeVariable)
			}

			// Generate sample MSISDNs
			fmt.Printf("Generating MSISDNs for column '%s':\n", column.Name)
			for _, networkCodeRange := range networkCodes {
				networkRange, ok := networkCodeRange.(string)
				if !ok {
					log.Fatalf("Network code '%v' is not a valid string", networkCodeRange)
				}

				// Parse and replace pattern
				tmpl, err := template.New("msisdn").Parse(column.Pattern)
				if err != nil {
					log.Fatalf("Error parsing pattern: %v", err)
				}

				// Simulate a subscriber number
				subscriberNumber := "1234567" // Example subscriber number

				// Resolve the template
				var result bytes.Buffer
				err = tmpl.Execute(&result, map[string]interface{}{
					"country_code": countryCode,
					"network_code": networkRange,
				})
				if err != nil {
					log.Fatalf("Error resolving template: %v", err)
				}

				// Print result
				fmt.Println(result.String() + "-" + subscriberNumber)
			}
		}
	}
}
