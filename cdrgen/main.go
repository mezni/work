package main

import (
	"errors"
	"fmt"
	"strconv"
	"strings"
)

// Define custom error variables
var (
	ErrInvalidType         = errors.New("invalid Type, expected 'NUMERIC'")
	ErrInvalidValuesFormat = errors.New("invalid Values format, expected [xxx]")
)

type NumericTypeInput struct {
	Type   string
	Values string
}

func (n *NumericTypeInput) validate() error {
	if strings.ToUpper(n.Type) != "NUMERIC" {
		return ErrInvalidType
	}

	_, err := strconv.Atoi(n.Values)
	if err == nil {
		return nil // valid integer, no further checks required
	}

	if !(strings.HasPrefix(n.Values, "[") && strings.HasSuffix(n.Values, "]")) {
		return ErrInvalidValuesFormat
	}
	insideValues := strings.Trim(n.Values, "[]")
	_, err = strconv.Atoi(insideValues)
	if err == nil {
		return nil // valid integer, no further checks required
	}

	valuesList := strings.Split(insideValues, ",")
	for _, val := range valuesList {
		fmt.Println(val)
	}

	return nil
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
	input := NewNumericTypeInput("numeric", "[1234,5678,text-a]")

	// Parse the input
	err := input.validate()
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	// Print the struct if parsing is successful
	fmt.Printf("Parsed Type: %s, Values: %s\n", input.Type, input.Values)
}
