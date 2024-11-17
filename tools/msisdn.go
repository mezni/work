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
  - name: called_party_number
    type: msisdn
    msisdn:
      country_code: [216,212]
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

func generateMSISDNTree(name string, config MSISDNConfig) error {
	countryCodes, err := getCountryCodes(config.CountryCode)
	if err != nil {
		return err
	}

	tree := CreateTreeNode(name)
	for _, cc := range countryCodes {
		countryCodeNode := CreateTreeNode(cc)
		AddChild(tree, countryCodeNode)
	}
	PrintTree(tree, 0)
	return nil
}

func getCountryCodes(countryCode interface{}) ([]string, error) {
	var countryCodes []string

	switch cc := countryCode.(type) {
	case []interface{}:
		for _, code := range cc {
			countryCodes = append(countryCodes, fmt.Sprintf("%v", code))
		}
	case string:
		countryCodes = append(countryCodes, cc)
	case int:
		countryCodes = append(countryCodes, fmt.Sprintf("%v", cc))
	default:
		countryCodes = append(countryCodes, defaultCountryCode)
	}

	return countryCodes, nil
}
