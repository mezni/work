package main

import (
	"fmt"
	"log"
	"math/rand"
	"strings"
	"time"

	"gopkg.in/yaml.v3"
)

const (
	defaultCountryCode = "216" // Tunisia's country code
	defaultNetworkCode = "50"  // OTN's network code
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

// PrintTree prints the tree
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
	// Initialize random number generator
	rand.Seed(time.Now().UnixNano())

	// Sample YAML configuration
	yamlConfig := `
columns:
  - name: test
    type: msisdn
  - name: calling_party_number
    type: msisdn
    msisdn:
      country_code: 216
      network_code: [50,51]
  - name: called_party_number
    type: msisdn
    msisdn:
      country_code: [216,212]
      network_code: 
        - 216: [50, 51]
        - 212: [06, 07]
`

	// Unmarshal YAML configuration
	var config Config
	err := yaml.Unmarshal([]byte(yamlConfig), &config)
	if err != nil {
		log.Printf("Error unmarshalling YAML configuration: %v", err)
		return
	}

	for _, column := range config.Columns {
		err := generateMSISDNTree(column.Name, column.MSISDN)
		if err != nil {
			log.Printf("Error generating MSISDN tree: %v", err)
			return
		}
	}
}

// generateMSISDNTree generates the MSISDN tree based on the provided configuration
func generateMSISDNTree(name string, config MSISDNConfig) error {
	// Get country codes and network codes from the configuration
	countryCodes, networkCodes, err := getMSISDNConfig(config)
	if err != nil {
		return err
	}

	// Create the tree structure
	tree := CreateTreeNode(name)
	for _, countryCode := range countryCodes {
		countryCodeNode := CreateTreeNode(countryCode)
		AddChild(tree, countryCodeNode)
		for _, networkCode := range networkCodes {
			networkCodeNode := CreateTreeNode(networkCode)
			AddChild(countryCodeNode, networkCodeNode)
		}
	}

	// Print the tree
	PrintTree(tree, 0)
	return nil
}

// getMSISDNConfig retrieves country codes and network codes from the provided configuration
func getMSISDNConfig(config MSISDNConfig) ([]string, []string, error) {
	var countryCodes []string
	var networkCodes []string

	// Get country codes
	countryCodes, err := getCountryCodes(config.CountryCode)
	if err != nil {
		return nil, nil, err
	}

	// Get network codes
	for _, countryCode := range countryCodes {
		network, err := getNetworkCodes(config.NetworkCode, countryCode)
		if err != nil {
			return nil, nil, err
		}
		networkCodes = append(networkCodes, network...)
	}

	return countryCodes, networkCodes, nil
}

// getCountryCodes retrieves country codes from the provided configuration
func getCountryCodes(countryCode interface{}) ([]string, error) {
	var countryCodes []string

	switch countryCode := countryCode.(type) {
	case []interface{}:
		for _, code := range countryCode {
			countryCodes = append(countryCodes, fmt.Sprintf("%v", code))
		}
	case string:
		countryCodes = append(countryCodes, countryCode)
	case int:
		countryCodes = append(countryCodes, fmt.Sprintf("%v", countryCode))
	default:
		countryCodes = append(countryCodes, defaultCountryCode)
	}

	return countryCodes, nil
}

// getNetworkCodes retrieves network codes from the provided configuration
func getNetworkCodes(networkCode interface{}, countryCode string) ([]string, error) {
	var networkCodes []string

	switch networkCode := networkCode.(type) {
	case []interface{}:
		for _, code := range networkCode {
			networkCodes = append(networkCodes, fmt.Sprintf("%v", code))
		}
	case string:
		networkCodes = append(networkCodes, networkCode)
	case int:
		networkCodes = append(networkCodes, fmt.Sprintf("%v", networkCode))
	case map[interface{}]interface{}:
		// Handle the map structure
		for k, v := range networkCode {
			if k == countryCode {
				switch v := v.(type) {
				case []interface{}:
					for _, code := range v {
						networkCodes = append(networkCodes, fmt.Sprintf("%v", code))
					}
				}
			}
		}
	default:
		networkCodes = append(networkCodes, defaultNetworkCode)
	}

	return networkCodes, nil
}
