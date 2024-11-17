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

func (n *TreeNode) FindChild(value string) *TreeNode {
	for _, child := range n.Children {
		if child.Value == value {
			return child
		}
	}
	return nil
}

func main() {
	generator := CreateTreeNode("msisdn")
	countryCode1 := CreateTreeNode("216")
	countryCode2 := CreateTreeNode("212")

	networkCode1 := CreateTreeNode("50")
	networkCode2 := CreateTreeNode("51")

	networkCode3 := CreateTreeNode("06")
	networkCode4 := CreateTreeNode("07")

	subscriberNum1 := CreateTreeNode("1234567890")
	subscriberNum2 := CreateTreeNode("9876543210")
	subscriberNum3 := CreateTreeNode("5555555555")

	AddChild(generator, countryCode1)
	AddChild(generator, countryCode2)

	AddChild(countryCode1, networkCode1)
	AddChild(countryCode1, networkCode2)

	AddChild(countryCode2, networkCode3)
	AddChild(countryCode2, networkCode4)
	AddChild(countryCode1, subscriberNum1)
	AddChild(countryCode1, subscriberNum2)
	AddChild(countryCode1, subscriberNum3)
	PrintTree(generator, 0)

	networkCode1 = generator.FindChild("216")
	fmt.Println(networkCode1.Value)
}