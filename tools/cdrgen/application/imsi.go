package application

import (
	"fmt"
	"github.com/mezni/bridge/tools/cdrgen/domain/services" 
)

func GenerateAndUseIMSI() {
	generator := services.NewIMSIGenerator()

	// Example MCC and MNC
	mcc := "310" // USA
	mnc := "260" // T-Mobile
	subscriberNumberLength := 9 // Length for the random subscriber number

	imsi, err := generator.GenerateIMSI(mcc, mnc, subscriberNumberLength)
	if err != nil {
		fmt.Println("Error generating IMSI:", err)
		return
	}

	fmt.Println("Generated IMSI:", imsi.String())
}
