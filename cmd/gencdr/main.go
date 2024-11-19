package main

import (
	"errors"
	"fmt"
	"strings"
)

// Column represents a database column
type Column struct {
	Name  string
	Type  string
	Start *int // Optional start value
	Step  *int // Optional step value
}

// ValidTypes defines the allowed column types
var ValidTypes = map[string]bool{
	"incremental": true,
	"numeric":     true,
	"string":      true,
	"boolean":     true, // New column type added
}

// validate checks if a column is valid
func (c *Column) validate() error {
	if strings.TrimSpace(c.Name) == "" {
		return errors.New("column name cannot be empty")
	}

	if !ValidTypes[c.Type] {
		return fmt.Errorf("invalid column type: %q", c.Type)
	}

	// Ensure start and step values are correct (if applicable)
	if c.Type == "incremental" {
		if c.Start == nil {
			return errors.New("start value is required for incremental type")
		}
		if c.Step == nil {
			return errors.New("step value is required for incremental type")
		}
	}

	return nil
}

// NewColumn creates a new column with the given name, type, start, and step
func NewColumn(name, colType string, start, step *int) (*Column, error) {
	// If column type is "incremental", set default values for start and step if they are nil
	if colType == "incremental" {
		if start == nil {
			defaultStart := 1
			start = &defaultStart
		}
		if step == nil {
			defaultStep := 1
			step = &defaultStep
		}
	}

	// Create the column with the provided values
	column := &Column{
		Name:  name,
		Type:  colType,
		Start: start,
		Step:  step,
	}

	// Validate the column
	if err := column.validate(); err != nil {
		return nil, err
	}
	return column, nil
}

func main() {

	// Test case with specific values for start and step
	start := 100
	step := 10
	// Example columns with start and step values
	columns := []struct {
		name, colType string
		start, step    *int
	}{
		{"username", "string", nil, nil},               // Valid
		{"", "invalidType", nil, nil},                  // Invalid
		{"id", "incremental", nil, nil},                // Valid (start and step handled by default)
		{"price", "unsupportedType", nil, nil},         // Invalid
		{"isActive", "boolean", nil, nil},              // Valid
		{"order_number", "incremental", nil, nil},      // Valid (start and step handled by default)
		{"order_number", "incremental", &start, &step}, // Updated test case with specific start and step values
	}

	// Iterate over the columns and create them
	for i, columnData := range columns {
		column, err := NewColumn(columnData.name, columnData.colType, columnData.start, columnData.step)
		if err != nil {
			fmt.Printf("Column %d validation failed: %v\n", i+1, err)
		} else {
			fmt.Printf("Column %d validation succeeded: %+v\n", i+1, column)
		}
	}

	// Create an incremental column with specific start and step values
	column, err := NewColumn("order_id", "incremental", &start, &step)
	if err != nil {
		fmt.Println("Error creating column:", err)
		return
	}

	// Print the column created with specific start and step values
	fmt.Printf("Column with specific start and step: %+v\n", column)

	// Create an incremental column with default start and step values (since start and step are nil)
	columnWithDefaults, err := NewColumn("order_number", "incremental", nil, nil)
	if err != nil {
		fmt.Println("Error creating column:", err)
		return
	}

	// Print the updated column created with default start and step values
	fmt.Printf("Column with default start and step: %+v\n", columnWithDefaults)
}
