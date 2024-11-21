package main

import (
	"fmt"
	"log"
	"gopkg.in/yaml.v3"
)

// Node represents a tree structure for the YAML document
type Node struct {
	Type     string       // Type of the node (scalar, map, sequence)
	Key      string       // For map nodes, the key
	Value    string       // For scalar nodes, the value
	Children []*Node      // Children nodes for map and sequence types
}

// Recursively parse YAML into a tree of nodes
func parseNode(yamlNode *yaml.Node) *Node {
	var n Node

	switch yamlNode.Kind {
	case yaml.ScalarNode:
		// Scalar node (single value like a string or number)
		n.Type = "scalar"
		n.Value = yamlNode.Value

	case yaml.MappingNode:
		// Mapping node (key-value pair)
		n.Type = "map"
		for i := 0; i < len(yamlNode.Content); i += 2 {
			// Content[i] is the key, Content[i+1] is the value
			keyNode := parseNode(yamlNode.Content[i])
			valueNode := parseNode(yamlNode.Content[i+1])
			keyNode.Children = append(keyNode.Children, valueNode) // Adding value as child of the key node
			n.Children = append(n.Children, keyNode)              // Adding the key-value pair to the map node
		}

	case yaml.SequenceNode:
		// Sequence node (array)
		n.Type = "sequence"
		for _, item := range yamlNode.Content {
			childNode := parseNode(item)
			n.Children = append(n.Children, childNode)
		}
	}
	return &n
}

// Print the tree structure recursively
func printTree(n *Node, indent string, level int) {
	// Print only level 2 nodes (second level in the tree)
	if level == 2 {
		fmt.Printf("%s[%s]: %s\n", indent, n.Type, n.Value)
	}
	for _, child := range n.Children {
		// Recursively print each child with increased indentation and incremented level
		printTree(child, indent+"  ", level+1)
	}
}

func main() {
	// Example YAML data (including the 'code' node and its children)
	yamlData := `
lookups:
  countries:
    rows: 100
    columns:
      name:
        values:
          - Canada
          - USA
          - Mexico
          - UK
          - Australia
        distribution:
          Canada: 0.2
          USA: 0.3
          Mexico: 0.1
          UK: 0.2
          Australia: 0.2
      code:
        values:
          - CA
          - US
          - MX
          - GB
          - AU
        distribution:
          CA: 0.2
          US: 0.3
          MX: 0.1
          GB: 0.2
          AU: 0.2
      mcc:
        values:
          - 302
          - 310
          - 334
          - 235
          - 505
        distribution:
          302: 0.2
          310: 0.3
          334: 0.1
          235: 0.2
          505: 0.2
      mnc:
        mapping:
          302:
            - 101
            - 102
          310:
            - 201
          334:
            - 301
          235:
            - 202
            - 203
          505:
            - 401
      phone_number:
        formula: "{{ mcc }}{{ mnc }}{{ random_number(6) }}"
`

	// Parse the YAML data into a YAML node
	var rootNode yaml.Node
	err := yaml.Unmarshal([]byte(yamlData), &rootNode)
	if err != nil {
		log.Fatalf("Error unmarshaling YAML: %v", err)
	}

	// Tokenize the YAML into a tree structure
	tree := parseNode(&rootNode)

	// Print the tree structure for the "lookups" root (level 2 nodes)
	printTree(tree, "", 0)
}
