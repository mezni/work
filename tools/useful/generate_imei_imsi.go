package main

import (
	"fmt"
	"math/rand"
	"strconv"
	"time"
)

// GenerateRandomIMSI generates a random IMSI (International Mobile Subscriber Identity)
func GenerateRandomIMSI(countryCode string, operatorCode string) string {
	// Generate a random 9-digit MSIN (Mobile Subscriber Identification Number)
	msin := fmt.Sprintf("%09d", rand.Intn(1000000000))

	// Return IMSI formatted as MCC + MNC + MSIN
	return fmt.Sprintf("%s%s%s", countryCode, operatorCode, msin)
}

// GenerateRandomIMEI generates a random IMEI (International Mobile Equipment Identity)
func GenerateRandomIMEI() string {
	// Generate a random 8-digit TAC (Type Allocation Code)
	tac := fmt.Sprintf("%08d", rand.Intn(100000000))

	// Generate a random 6-digit Serial Number
	serial := fmt.Sprintf("%06d", rand.Intn(1000000))

	// Calculate the check digit using the Luhn algorithm
	checkDigit := calculateIMEICheckDigit(tac + serial)

	// Return IMEI formatted as TAC + Serial + Check Digit
	return fmt.Sprintf("%s%s%d", tac, serial, checkDigit)
}

// Luhn algorithm to calculate the check digit for IMEI
func calculateIMEICheckDigit(imeiWithoutCheckDigit string) int {
	sum := 0
	// Iterate over the digits in reverse order
	for i, digit := range imeiWithoutCheckDigit {
		num, _ := strconv.Atoi(string(digit))
		if i%2 == len(imeiWithoutCheckDigit)%2 {
			// Double every second digit from the right (or left, depending on even/odd position)
			num = num * 2
			if num > 9 {
				num -= 9
			}
		}
		sum += num
	}
	// The check digit is the number that, when added to the sum, makes it a multiple of 10
	return (10 - (sum % 10)) % 10
}

func main() {
	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	// Define inputs for IMSI generation
	countryCode := "216" // MCC for Tunisia
	operatorCode := "01" // Example MNC for an operator in Tunisia

	// Generate IMSI and IMEI
	imsi := GenerateRandomIMSI(countryCode, operatorCode)
	imei := GenerateRandomIMEI()

	// Print the generated IMSI and IMEI
	fmt.Println("Random IMSI:", imsi)
	fmt.Println("Random IMEI:", imei)
}
