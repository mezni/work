package core

import (
	"testing"

	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
)

// TestNewDataRecord_Success tests successful creation of a DataRecord
func TestNewDataRecord_Success(t *testing.T) {
	data := DataMap{
		"name": "Test Record",
		"age":  30,
	}
	requiredKeys := []string{"name", "age"}

	record, err := NewDataRecord(data, requiredKeys)

	assert.NoError(t, err)
	assert.NotEqual(t, uuid.Nil, record.ID, "ID should not be nil")
	assert.Equal(t, "Test Record", record.Data["name"])
	assert.Equal(t, 30, record.Data["age"])
	assert.Equal(t, record.ID.String(), record.Data["id"])
}

// TestNewDataRecord_MissingKey tests failure due to missing required keys
func TestNewDataRecord_MissingKey(t *testing.T) {
	data := DataMap{
		"name": "Test Record",
	}
	requiredKeys := []string{"name", "age"} // "age" is missing

	_, err := NewDataRecord(data, requiredKeys)

	assert.Error(t, err)
	assert.Contains(t, err.Error(), ErrMissingKey.Error())
}

// TestValidate_Success tests successful validation of a DataRecord
func TestValidate_Success(t *testing.T) {
	data := DataMap{
		"name": "Test Record",
		"age":  30,
	}
	record := DataRecord{
		ID:   uuid.New(),
		Data: data,
	}
	requiredKeys := []string{"name", "age"}

	err := record.Validate(requiredKeys)

	assert.NoError(t, err)
}

// TestValidate_InvalidID tests validation failure due to an invalid ID
func TestValidate_InvalidID(t *testing.T) {
	data := DataMap{
		"name": "Test Record",
		"age":  30,
	}
	record := DataRecord{
		ID:   uuid.Nil, // Invalid UUID
		Data: data,
	}
	requiredKeys := []string{"name", "age"}

	err := record.Validate(requiredKeys)

	assert.Error(t, err)
	assert.Equal(t, ErrInvalidID, err)
}

// TestValidate_MissingKey tests validation failure due to missing required keys
func TestValidate_MissingKey(t *testing.T) {
	data := DataMap{
		"name": "Test Record",
	}
	record := DataRecord{
		ID:   uuid.New(),
		Data: data,
	}
	requiredKeys := []string{"name", "age"} // "age" is missing

	err := record.Validate(requiredKeys)

	assert.Error(t, err)
	assert.Contains(t, err.Error(), ErrMissingKey.Error())
}

// TestNewDataRecord_EmptyMap tests creation of DataRecord with an empty data map
func TestNewDataRecord_EmptyMap(t *testing.T) {
	data := DataMap{}
	requiredKeys := []string{"name", "age"} // Both keys are missing

	_, err := NewDataRecord(data, requiredKeys)

	assert.Error(t, err)
	assert.Contains(t, err.Error(), ErrMissingKey.Error())
}
