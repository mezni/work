package main

import (
	"fmt"
	"strings"
)

type TreeNode struct {
	Value    string
	Children []*TreeNode
}

func CreateTreeNode(value string) *TreeNode {
	return &TreeNode{Value: value, Children: make([]*TreeNode, 0)}
}

func AddChild(parent *TreeNode, child *TreeNode) {
	parent.Children = append(parent.Children, child)
}

func PrintTree(node *TreeNode, level int) {
	fmt.Printf("%s%s\n", strings.Repeat("  ", level), node.Value)
	for _, child := range node.Children {
		PrintTree(child, level+1)
	}
}

func (n *TreeNode) PrintPrefixes(root string) []string {
	if root == "" {
		return []string{"21650"}
	}

	if len(n.Children) == 0 {
		return []string{n.Value}
	}

	var prefixes []string
	for _, child := range n.Children {
		for _, prefix := range child.PrintPrefixes(root) {
			if n.Value != root {
				prefixes = append(prefixes, n.Value+prefix)
			} else {
				prefixes = append(prefixes, prefix)
			}
		}
	}
	return prefixes
}

func (n *TreeNode) FindChild(value string) *TreeNode {
	if n.Value == value {
		return n
	}
	for _, child := range n.Children {
		found := child.FindChild(value)
		if found != nil {
			return found
		}
	}
	return nil
}

func main() {
	root := CreateTreeNode("local_msisdn")
	countryCode := CreateTreeNode("216")
	AddChild(root, countryCode)

	networkCode1 := CreateTreeNode("50")
	networkCode2 := CreateTreeNode("51")

	AddChild(countryCode, networkCode1)
	AddChild(countryCode, networkCode2)
	//	PrintTree(root, 0)

	prefixes := root.PrintPrefixes("local_msisdn")
	fmt.Println("Prefixes (excluding root):")
	for _, prefix := range prefixes {
		fmt.Println(prefix)
	}
}
