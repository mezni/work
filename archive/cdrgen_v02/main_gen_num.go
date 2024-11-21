package main

import (
	"errors"
	"fmt"
	"math/rand"
	"regexp"
	"strconv"
	"strings"
	"time"
)

// Define custom error variables
var (
	ErrInvalidType         = errors.New("invalid Type, expected 'NUMERIC'")
	ErrInvalidValuesFormat = errors.New("invalid Values format, expected [xxx]")
	ErrInvalidValue        = errors.New("invalid Value, expected numeric")
	ErrInvalidRange        = errors.New("invalid Range, start should be less than stop")
)

// Helper function to check if a string represents a valid integer
func isInt(s string) bool {
	_, err := strconv.Atoi(s)
	return err == nil
}

type NumericTypeInput struct {
	Type   string
	Values string
}

func (n *NumericTypeInput) validate() error {
	// Check if Type is "NUMERIC"
	if strings.ToUpper(n.Type) != "NUMERIC" {
		return ErrInvalidType
	}

	// Check if Values is a valid integer
	if isInt(n.Values) {
		return nil // valid integer, no further checks required
	}

	// Check if Values is in the list format [xxx,yyy,...]
	if !(strings.HasPrefix(n.Values, "[") && strings.HasSuffix(n.Values, "]")) {
		return ErrInvalidValuesFormat
	}

	// Remove the square brackets from the Values string
	insideValues := strings.Trim(n.Values, "[]")
	// Check if the whole insideValues is a valid integer
	if isInt(insideValues) {
		return nil // valid integer, no further checks required
	}

	// Split the Values string into individual elements (by commas)
	valuesList := strings.Split(insideValues, ",")
	for _, val := range valuesList {
		// Check if the value contains a range (e.g., "1-5" or "1:5")
		if strings.Contains(val, ":") || strings.Contains(val, "-") {
			// Split the range by "-" or ":"
			re := regexp.MustCompile(`[:\-]`)
			parts := re.Split(val, -1)
			if len(parts) != 2 {
				return ErrInvalidValuesFormat // Invalid range format
			}
			start := parts[0]
			stop := parts[1]

			// Validate the start and stop values of the range
			if !isInt(start) {
				return ErrInvalidValue // Invalid start value
			}
			if !isInt(stop) {
				return ErrInvalidValue // Invalid stop value
			}

			// Convert start and stop to integers for comparison
			startInt, _ := strconv.Atoi(start)
			stopInt, _ := strconv.Atoi(stop)

			// Check if start is less than stop
			if startInt >= stopInt {
				return ErrInvalidRange // start should be less than stop
			}
		} else {
			// Otherwise, validate the individual value
			if !isInt(val) {
				return ErrInvalidValue // Invalid value
			}
		}
	}

	return nil
}

func (n *NumericTypeInput) Generate() (string, error) {
	var listNumeric []int

	// Check if Values is a valid integer
	if isInt(n.Values) {
		randomNumericInt, _ := strconv.Atoi(n.Values)
		return strconv.Itoa(randomNumericInt), nil
	} else {
		// Handle the list format, e.g., [1234,5678,1-5,3-10]
		insideValues := strings.Trim(n.Values, "[]")
		valuesList := strings.Split(insideValues, ",")
		for _, val := range valuesList {
			if strings.Contains(val, ":") || strings.Contains(val, "-") {
				// Parse the range and generate values
				re := regexp.MustCompile(`[:\-]`)
				parts := re.Split(val, -1)
				start, _ := strconv.Atoi(parts[0])
				stop, _ := strconv.Atoi(parts[1])
				// Generate numbers in the range
				for i := start; i <= stop; i++ {
					listNumeric = append(listNumeric, i)
				}
			} else {
				// Single value, just add it
				num, _ := strconv.Atoi(val)
				listNumeric = append(listNumeric, num)
			}
		}
	}

	// If the listNumeric has numbers, select a random value
	if len(listNumeric) > 0 {
		// Seed the random number generator (this ensures randomness each time the program runs)
		rand.Seed(time.Now().UnixNano())
		// Generate a random index
		randomIndex := rand.Intn(len(listNumeric))
		randomNumericInt := listNumeric[randomIndex]
		return strconv.Itoa(randomNumericInt), nil
	}

	// If listNumeric is empty, return an error
	return "", errors.New("no numeric values to generate")
}

// Constructor function to initialize the struct
func NewNumericTypeInput(typeVal, valuesVal string) NumericTypeInput {
	return NumericTypeInput{
		Type:   typeVal,
		Values: valuesVal,
	}
}

func main() {
	// Example input
	input := NewNumericTypeInput("NUMERIC", "[1234,5678,1-5,3-10]")

	// Parse the input
	err := input.validate()
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	// Print the struct if parsing is successful
	fmt.Printf("Parsed Type: %s, Values: %s\n", input.Type, input.Values)

	// Generate a value
	randomValue, err := input.Generate()
	if err != nil {
		fmt.Println("Error generating value:", err)
		return
	}

	fmt.Println("Generated Value:", randomValue)
}
