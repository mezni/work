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
		err := generateMSISDNTree(column)
		if err != nil {
			log.Printf("Error generating MSISDN tree: %v", err)
			return
		}
	}
}

func generateMSISDNTree(config ColumnConfig) error {
	fmt.Println("#####")
	fmt.Printf("Generating MSISDN tree for column: %s\n", config.Name)

	var countryCodes []string
	var networkCodes []string

	// Get country codes
	countryCodes, err := getCountryCodes(config.MSISDN.CountryCode)
	if err != nil {
		return err
	}

	// Get network codes
	networkCodes, err = getNetworkCodes(config.MSISDN.NetworkCode)
	if err != nil {
		return err
	}
	// WORK
	fmt.Println("Root:", config.Name)
	fmt.Println("Country Codes:", countryCodes)
	fmt.Println("Network Codes:", networkCodes)

	for _, networkCode := range networkCodes {
		fmt.Println(networkCode)
		fmt.Printf("Type of networkCode: %T\n", networkCode)
	}
	/*
		// Create MSISDN tree
		root := CreateTreeNode("MSISDN")
		for _, countryCode := range countryCodes {
			countryNode := CreateTreeNode(countryCode)
			AddChild(root, countryNode)
			for _, networkCode := range networkCodes {
				networkNode := CreateTreeNode(networkCode)
				AddChild(countryNode, networkNode)
			}
		}

		// Print MSISDN tree
		PrintTree(root, 0)
	*/
	return nil
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

func getNetworkCodes(networkCode interface{}) ([]string, error) {
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
	default:
		networkCodes = append(networkCodes, defaultNetworkCode)
	}

	return networkCodes, nil
}
