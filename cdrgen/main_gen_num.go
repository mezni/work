package main

import (
	"errors"
	"fmt"
	"math/rand"
	"strconv"
	"strings"
	"time"
)

// Function to parse either a list or a range, a single value, or handle an empty input
func parseInput(input string) ([]int, error) {
	// Trim spaces
	input = strings.TrimSpace(input)

	// If the input is an empty string, return a random number as a list
	if input == "" {
		return []int{rand.Intn(100)}, nil // Random number between 0 and 99
	}

	// If the input contains a comma, it's a list
	if strings.Contains(input, ",") {
		// Remove square brackets
		input = strings.Trim(input, "[]")
		// Split by comma to create a list
		parts := strings.Split(input, ",")
		var result []int
		for _, part := range parts {
			// Trim spaces and convert to integer
			num, err := strconv.Atoi(strings.TrimSpace(part))
			if err != nil {
				return nil, fmt.Errorf("could not convert %s to integer: %v", part, err)
			}
			result = append(result, num)
		}
		return result, nil
	}

	// If the input contains a colon, it's a range
	if strings.Contains(input, ":") {
		// Split by colon to create the range
		parts := strings.Split(input, ":")
		if len(parts) != 2 {
			return nil, errors.New("invalid range format, should be start:end")
		}
		start, err1 := strconv.Atoi(strings.TrimSpace(parts[0]))
		end, err2 := strconv.Atoi(strings.TrimSpace(parts[1]))
		if err1 != nil || err2 != nil {
			return nil, fmt.Errorf("could not convert range values to integers: %v, %v", err1, err2)
		}

		// Create a range of numbers
		var result []int
		for i := start; i <= end; i++ {
			result = append(result, i)
		}
		return result, nil
	}

	// If the input does not contain a comma or colon, treat it as a single value
	num, err := strconv.Atoi(input)
	if err != nil {
		return nil, fmt.Errorf("could not convert '%s' to integer: %v", input, err)
	}
	return []int{num}, nil
}

// Function to return a random value from the list
func getRandomValue(list []int) int {
	rand.Seed(time.Now().UnixNano())    // Initialize the random seed
	randomIndex := rand.Intn(len(list)) // Get a random index
	return list[randomIndex]            // Return the random value
}

func main() {
	// Test cases
	tests := []string{
		"[1,2,3]",
		"1:5",
		"[10,20,30]",
		"7:10",
		"5", // Single value
		"",  // Empty string, should generate random number
	}

	for _, test := range tests {
		result, err := parseInput(test)
		if err != nil {
			fmt.Printf("Error parsing '%s': %v\n", test, err)
		} else {
			fmt.Printf("Parsed '%s' to: %v\n", test, result)
			randomValue := getRandomValue(result)
			fmt.Printf("Random value from list: %d\n", randomValue)
		}
	}
}


package main

import (
	"errors"
	"fmt"
)

// Error variables
var (
	ErrNameMissing   = errors.New("key 'name' does not exist")
	ErrNameNotString = errors.New("key 'name' exists but is not a string")
	ErrNameEmpty     = errors.New("key 'name' exists but is an empty string")
	ErrValuesMissing = errors.New("key 'values' does not exist")
)

// Define the GeneratorArg type
type GeneratorArg map[string]interface{}

// Define the NumericGenerator function with error handling
func NumericGenerator(args GeneratorArg) error {
	// Check if "name" key exists
	name, ok := args["name"]
	if !ok {
		return ErrNameMissing
	}

	// Check if the value of "name" is a string
	strName, isString := name.(string)
	if !isString {
		return ErrNameNotString
	}

	// Check if the string is non-empty
	if strName == "" {
		return ErrNameEmpty
	}

	// Check if "values" key exists
	if _, ok := args["values"]; !ok {
		return ErrValuesMissing
	}

	return nil
}

// Main function to demonstrate usage
func main() {
	// Test case 1: Valid arguments
	args := GeneratorArg{
		"name":   "TestGenerator",
		"values": []int{1, 2, 3, 4, 5},
	}
	if err := NumericGenerator(args); err != nil {
		fmt.Println("Error:", err)
	} else {
		fmt.Println("Arguments are valid.")
	}

	fmt.Println()

	// Test case 2: "name" is not a string
	argsNotStringName := GeneratorArg{
		"name":   123,
		"values": []int{10, 20, 30},
	}
	if err := NumericGenerator(argsNotStringName); err != nil {
		fmt.Println("Error:", err)
	} else {
		fmt.Println("Arguments are valid.")
	}

	fmt.Println()

	// Test case 3: Empty "name"
	argsEmptyName := GeneratorArg{
		"name":   "",
		"values": []int{10, 20, 30},
	}
	if err := NumericGenerator(argsEmptyName); err != nil {
		fmt.Println("Error:", err)
	} else {
		fmt.Println("Arguments are valid.")
	}

	fmt.Println()

	// Test case 4: Missing "name" key
	argsNoName := GeneratorArg{
		"values": []int{100, 200, 300},
	}
	if err := NumericGenerator(argsNoName); err != nil {
		fmt.Println("Error:", err)
	} else {
		fmt.Println("Arguments are valid.")
	}
}


package main

import (
	"fmt"
)

// Define the GeneratorArg type
type GeneratorArg map[string]interface{}

// Validator function for validating the arguments
func validateArgs(args GeneratorArg) error {
	// Check if "name" key exists and is a non-empty string (spaces allowed)
	if name, ok := args["name"].(string); !ok || name == "" {
		return fmt.Errorf("invalid 'name' value: must be a non-empty string")
	}

	// Check if "values" key exists and is an integer
	if _, ok := args["values"].(int); !ok {
		return fmt.Errorf("invalid 'values' value: must be an integer")
	}

	return nil
}

// Function renamed to NumericGenerator
func NumericGenerator(args GeneratorArg) {
	// Validate arguments
	if err := validateArgs(args); err != nil {
		fmt.Println("Error:", err)
		return
	}

	// Iterate over the map and print the key-value pairs
	for key, value := range args {
		fmt.Printf("%s: %v\n", key, value)
	}
}

func main() {
	// Create an instance of GeneratorArg with valid data (name with space)
	args := GeneratorArg{
		"name":   "Cell ID 123",
		"values": 28,
	}
	name, ok := args["name"].(string)
	fmt.Println(name, ok)
	// Call the renamed function with GeneratorArg
	NumericGenerator(args)

	// Create an instance of GeneratorArg with invalid data (missing or incorrect value)
	invalidArgs := GeneratorArg{
		"name":   "",
		"values": "not an int", // This will fail validation
	}

	// Call the function with invalid args
	NumericGenerator(invalidArgs)
}

package main

import (
	"fmt"

)

// Define the GeneratorArg type
type GeneratorArg map[string]interface{}

// Validator function for validating the arguments
func validateArgs(args GeneratorArg) error {
	// Check if "name" key exists and is a non-empty string (spaces allowed)
	fmt.Println(args["name"].(string))
	if name, ok := args["name"].(string); !ok || name == "" {
	fmt.Println("XXXX")
	
	fmt.Println(ok ,name )
		return fmt.Errorf("invalid 'name' value: must be a non-empty string")
	}

	// Check if "values" key exists and is an integer
	if _, ok := args["values"].(int); !ok {
		return fmt.Errorf("invalid 'values' value: must be an integer")
	}

	return nil
}

// Function renamed to NumericGenerator
func NumericGenerator(args GeneratorArg) {
	// Validate arguments
	if err := validateArgs(args); err != nil {
		fmt.Println("Error:", err)
		return
	}

	// Iterate over the map and print the key-value pairs
	for key, value := range args {
		fmt.Printf("%s: %v\n", key, value)
	}
}

func main() {
	// Create an instance of GeneratorArg with valid data (name with space)
	args := GeneratorArg{
		"name":   "Cell ID",
		"values": 28,
	}

	// Call the renamed function with GeneratorArg
	NumericGenerator(args)

	// Create an instance of GeneratorArg with invalid data (missing or incorrect value)
	invalidArgs := GeneratorArg{
		"name":   "",
		"values": "not an int", // This will fail validation
	}

	// Call the function with invalid args
	NumericGenerator(invalidArgs)
}
