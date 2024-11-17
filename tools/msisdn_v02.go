package main

import (
	"fmt"
	"strings"
)

func NewMSISDN(countryCode int, networkCode int, subscriberNumber int, numberPattern string) string {

	pattern := strings.Replace(numberPattern, "XXX", "%d", 1)
	pattern = strings.Replace(pattern, "XX", "%d", 1)
	pattern = strings.Replace(pattern, "XXXXXX", "%d", 1)

	return fmt.Sprintf(pattern, countryCode, networkCode, subscriberNumber)

}

func main() {

	msisdn := NewMSISDN(216, 50, 350350, "+XXXXXXXXXXX")

	fmt.Println(msisdn)
}