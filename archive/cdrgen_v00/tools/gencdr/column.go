package gencdr

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