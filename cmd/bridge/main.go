package main

import (
	"fmt"
	"github.com/mezni/bridge/internal/msisdn"
)

func main() {
	prefixes := []string{"21650", "21651"}
	digits := 6
	localFlag := true
	generator := msisdn.NewMSISDNConfig(prefixes, digits)
	generator.SetLocal(localFlag)
	msisdn := generator.Generate()
	fmt.Println(msisdn)

	msisdns := generator.GenerateList(10)
	fmt.Println(msisdns)
}
