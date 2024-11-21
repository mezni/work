package msisdn

import (
	"fmt"
	"strings"
)

// TreeNode represents a node in the tree.
type TreeNode struct {
	Value    string
	Children []*TreeNode
}

// CreateTreeNode creates a new TreeNode with the given value.
func CreateTreeNode(value string) *TreeNode {
	return &TreeNode{Value: value, Children: make([]*TreeNode, 0)}
}

// AddChild adds a child node to the parent node.
func AddChild(parent *TreeNode, child *TreeNode) {
	parent.Children = append(parent.Children, child)
}

// PrintTree prints the tree with indentation.
func PrintTree(node *TreeNode, level int) {
	fmt.Printf("%s%s\n", strings.Repeat("  ", level), node.Value)
	for _, child := range node.Children {
		PrintTree(child, level+1)
	}
}

// FindChild finds a child node with the given value.
func (node *TreeNode) FindChild(value string) *TreeNode {
	if node.Value == value {
		return node
	}
	for _, child := range node.Children {
		if found := child.FindChild(value); found != nil {
			return found
		}
	}
	return nil
}