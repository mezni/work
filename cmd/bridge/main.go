package main

import (
	"fmt"
	"github.com/mezni/bridge/internal/msisdn"
)

func main() {
	fmt.Println("Prefixes:")
	root := msisdn.CreateTreeNode("local_msisdn")
	fmt.Println(root)
}
