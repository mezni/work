package gencdr

import (
	"testing"
	"fmt"
)

func TestNewColumn(t *testing.T) {
	// Define a table of test cases
	tests := []struct {
		name     string
		colType  string
		start    *int
		step     *int
		expected *Column
		err      error
	}{
		{
			name:    "valid string column",
			colType: "string",
			start:   nil,
			step:    nil,
			expected: &Column{
				Name:  "username",
				Type:  "string",
				Start: nil,
				Step:  nil,
			},
			err: nil,
		},
		{
			name:    "invalid type",
			colType: "invalidType",
			start:   nil,
			step:    nil,
			expected: nil,
			err:      fmt.Errorf("invalid column type: \"invalidType\""),
		},
		{
			name:    "valid incremental column with default start and step",
			colType: "incremental",
			start:   nil,
			step:    nil,
			expected: &Column{
				Name:  "order_number",
				Type:  "incremental",
				Start: intPointer(1),
				Step:  intPointer(1),
			},
			err: nil,
		},
		{
			name:    "valid incremental column with specific start and step",
			colType: "incremental",
			start:   intPointer(10),
			step:    intPointer(2),
			expected: &Column{
				Name:  "order_number",
				Type:  "incremental",
				Start: intPointer(10),
				Step:  intPointer(2),
			},
			err: nil,
		},
		{
			name:    "incremental missing start",
			colType: "incremental",
			start:   nil,
			step:    nil,
			expected: nil,
			err:      fmt.Errorf("start value is required for incremental type"),
		},
		{
			name:    "incremental missing step",
			colType: "incremental",
			start:   intPointer(1),
			step:    nil,
			expected: nil,
			err:      fmt.Errorf("step value is required for incremental type"),
		},
	}

	// Run each test case
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			column, err := NewColumn(tt.name, tt.colType, tt.start, tt.step)

			// Check if we got the expected error
			if err != nil && err.Error() != tt.err.Error() {
				t.Errorf("Expected error %v, but got %v", tt.err, err)
			}

			// If no error, check if the column matches the expected values
			if err == nil && *column != *tt.expected {
				t.Errorf("Expected column %+v, but got %+v", tt.expected, column)
			}
		})
	}
}

// Helper function to create a pointer to an int
func intPointer(i int) *int {
	return &i
}
