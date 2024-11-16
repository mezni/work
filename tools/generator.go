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