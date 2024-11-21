package core

import (
	"testing"

	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
)

// TestNewRepository ensures that the repository is initialized correctly
func TestNewRepository(t *testing.T) {
	repo := NewRepository()

	assert.NotNil(t, repo, "Repository should not be nil")
	assert.NotNil(t, repo.Records, "Records map should be initialized")
	assert.Equal(t, 0, len(repo.Records), "Repository should be empty on initialization")
}

// TestAddRecord_Success tests adding a record to the repository
func TestAddRecord_Success(t *testing.T) {
	repo := NewRepository()

	data := DataMap{
		"name": "Test Record",
		"age":  30,
	}
	requiredKeys := []string{"name", "age"}

	err := repo.AddRecord(data, requiredKeys)

	assert.NoError(t, err)
	assert.Equal(t, 1, len(repo.Records), "Repository should contain one record")
	for _, record := range repo.Records {
		assert.Equal(t, "Test Record", record.Data["name"])
		assert.Equal(t, 30, record.Data["age"])
	}
}

// TestAddRecord_MissingKey tests that adding a record fails when required keys are missing
func TestAddRecord_MissingKey(t *testing.T) {
	repo := NewRepository()

	data := DataMap{
		"name": "Test Record",
	}
	requiredKeys := []string{"name", "age"} // "age" is missing

	err := repo.AddRecord(data, requiredKeys)

	assert.Error(t, err)
	assert.Equal(t, 0, len(repo.Records), "Repository should remain empty when record creation fails")
}

// TestGetRecord_Success tests retrieving an existing record from the repository
func TestGetRecord_Success(t *testing.T) {
	repo := NewRepository()

	data := DataMap{
		"name": "Test Record",
		"age":  30,
	}
	requiredKeys := []string{"name", "age"}
	err := repo.AddRecord(data, requiredKeys)
	assert.NoError(t, err)

	// Retrieve the added record
	var addedRecord DataRecord
	for _, record := range repo.Records { // Get the added record
		addedRecord = record
		break
	}

	retrievedRecord, err := repo.GetRecord(addedRecord.ID)

	assert.NoError(t, err)
	assert.Equal(t, addedRecord, retrievedRecord, "Retrieved record should match the added record")
}

// TestGetRecord_NotFound tests retrieval of a non-existing record
func TestGetRecord_NotFound(t *testing.T) {
	repo := NewRepository()

	randomID := uuid.New()

	_, err := repo.GetRecord(randomID)

	assert.Error(t, err)
	assert.Equal(t, ErrRecordNotFound, err)
}
