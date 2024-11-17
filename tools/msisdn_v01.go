package main

import (
	"fmt"
)

type MSISDN struct {
	countryCode      int
	networkCode      int
	subscriberNumber int
}


func NewMSISDN(countryCode int, networkCode int,subscriberNumber int ) MSISDNGenerator {
    return MSISDN{
        CountryCode:  countryCode,
        networkCode: networkCode,
        subscriberNumber: subscriberNumber,        
    }
}

func main() {

msisdn := NewMSISDN(216, 50, 135350)
	internationalCallPrefix := "+"

	fmt.Println(internationalCallPrefix, msisdn)
}