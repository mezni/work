package main

import (
	"fmt"
	"log"
	"strings"

	"gopkg.in/yaml.v3"
)

const (
	defaultCountryCode = "216" // Default country code
	defaultNetworkCode = "50"  // Default network code
)

// TreeNode represents a node in the tree
type TreeNode struct {
	Value    string
	Children []*TreeNode
}

// CreateTreeNode creates a new tree node
func CreateTreeNode(value string) *TreeNode {
	return &TreeNode{Value: value, Children: make([]*TreeNode, 0)}
}

// AddChild adds a child node to the tree
func AddChild(parent *TreeNode, child *TreeNode) {
	parent.Children = append(parent.Children, child)
}

// PrintTree prints the tree in a hierarchical format
func PrintTree(node *TreeNode, level int) {
	fmt.Printf("%s%s\n", strings.Repeat("  ", level), node.Value)
	for _, child := range node.Children {
		PrintTree(child, level+1)
	}
}

// MSISDNConfig represents the configuration for generating MSISDNs
type MSISDNConfig struct {
	CountryCode interface{} `yaml:"country_code"`
	NetworkCode interface{} `yaml:"network_code"`
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
  - name: test
    type: msisdn
  - name: calling_party_number
    type: msisdn
    msisdn:
      country_code: 216
      network_code: [50, 51]
  - name: called_party_number
    type: msisdn
    msisdn:
      country_code: [216, 212]
      network_code: 
        - 216: [50, 51]
        - 212: [06, 07]
`

	// Unmarshal YAML configuration
	var config Config
	err := yaml.Unmarshal([]byte(yamlConfig), &config)
	if err != nil {
		log.Fatalf("Error unmarshalling YAML configuration: %v", err)
	}

	// Process each column
	for _, column := range config.Columns {
		err := generateMSISDNTree(column)
		if err != nil {
			log.Printf("Error generating MSISDN tree for column '%s': %v", column.Name, err)
		}
	}
}

// generateMSISDNTree builds and prints an MSISDN tree for a given column
func generateMSISDNTree(config ColumnConfig) error {
	fmt.Printf("\nGenerating MSISDN tree for column: %s\n", config.Name)

	// Root node for the tree
	root := CreateTreeNode(config.Name)

	// Extract country codes
	countryCodes, err := getCountryCodes(config.MSISDN.CountryCode)
	if err != nil {
		return err
	}

	// Process each country code
	for _, countryCode := range countryCodes {
		countryNode := CreateTreeNode(fmt.Sprintf("Country: %s", countryCode))
		AddChild(root, countryNode)

		// Extract network codes specific to the country
		networkCodes, err := getNetworkCodesForCountry(countryCode, config.MSISDN.NetworkCode)
	
		if err != nil {
			return err
		}

		// Add network codes as child nodes
		for _, networkCode := range networkCodes {
				fmt.Printf(networkCode)
			networkNode := CreateTreeNode(fmt.Sprintf("Network: %s", networkCode))
			AddChild(countryNode, networkNode)
		}
	}

	// Print the generated tree
	PrintTree(root, 0)
	return nil
}

// getCountryCodes retrieves country codes from the configuration
func getCountryCodes(input interface{}) ([]string, error) {
	return extractValues(input, []string{defaultCountryCode})
}

// getNetworkCodesForCountry retrieves network codes for a specific country
func getNetworkCodesForCountry(country string, input interface{}) ([]string, error) {
	switch v := input.(type) {
	case []interface{}:
		for _, item := range v {
			if itemMap, ok := item.(map[interface{}]interface{}); ok {
				if networks, found := itemMap[country]; found {
					return extractValues(networks, []string{defaultNetworkCode})
				}
			}
		}
		// No specific match found
		return []string{defaultNetworkCode}, nil
	default:
		// Handle non-hierarchical configurations
		return extractValues(input, []string{defaultNetworkCode})
	}
}

// extractValues converts input to a slice of strings with default fallback
func extractValues(input interface{}, defaultValues []string) ([]string, error) {
	var values []string

	switch v := input.(type) {
	case []interface{}: // List of values
		for _, item := range v {
			values = append(values, fmt.Sprintf("%v", item))
		}
	case string, int: // Single value
		values = append(values, fmt.Sprintf("%v", v))
	case nil: // Default values
		return defaultValues, nil
	default: // Unexpected types
		return nil, fmt.Errorf("unexpected type: %T", v)
	}

	return values, nil
}
