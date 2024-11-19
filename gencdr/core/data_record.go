package core

import (
	"errors"
	"fmt"
	"github.com/google/uuid"
)

// Define a custom type for the map to store dynamic data
type DataMap map[string]interface{}

// Predefined error variables
var (
	ErrInvalidID      = errors.New("invalid ID: UUID is empty")
	ErrMissingKey     = errors.New("invalid Data: missing required key")
	ErrRecordNotFound = errors.New("record not found") // This is used in the repository
)

// Define the DataRecord struct with ID as uuid.UUID and Data as DataMap
type DataRecord struct {
	ID   uuid.UUID // ID field of type UUID
	Data DataMap    // Data field of type map[string]interface{}
}

// NewDataRecord is a constructor function that initializes a DataRecord and validates it
func NewDataRecord(data DataMap, requiredKeys []string) (DataRecord, error) {
	// Generate a new UUID for the DataRecord
	newID := uuid.New()

	// Add the ID to the data map
	data["id"] = newID.String() // Store the ID as a string in the map (you can also use other formats as per your needs)

	// Create the DataRecord
	record := DataRecord{
		ID:   newID,
		Data: data,
	}

	// Validate the DataRecord
	if err := record.Validate(requiredKeys); err != nil {
		return DataRecord{}, err // Return an empty DataRecord and the validation error
	}

	// Return the valid DataRecord
	return record, nil
}

// Validate checks if the DataRecord has valid fields and if all required keys are present in the Data map
func (dr *DataRecord) Validate(requiredKeys []string) error {
	// Check if the ID is empty (UUID is all zeros)
	if dr.ID == uuid.Nil {
		return ErrInvalidID
	}

	// Check if all required keys are present in the Data map
	for _, key := range requiredKeys {
		if _, exists := dr.Data[key]; !exists {
			return fmt.Errorf("%w: '%s'", ErrMissingKey, key) // Return an error for the missing key
		}
	}

	// If all validations pass, return nil (no error)
	return nil
}

