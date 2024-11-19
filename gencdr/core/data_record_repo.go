package core

import (
	"github.com/google/uuid"
)

// Define a simple in-memory repository for DataRecords
type Repository struct {
	Records map[uuid.UUID]DataRecord // Change to uppercase 'Records' so it's public
}

// NewRepository creates and returns a new repository
func NewRepository() *Repository {
	return &Repository{
		Records: make(map[uuid.UUID]DataRecord), // Initialize the map
	}
}

// AddRecord adds a new DataRecord to the repository
func (repo *Repository) AddRecord(data DataMap, requiredKeys []string) error {
	record, err := NewDataRecord(data, requiredKeys)
	if err != nil {
		return err
	}
	repo.Records[record.ID] = record
	return nil
}

// GetRecord retrieves a DataRecord by its ID from the repository
func (repo *Repository) GetRecord(id uuid.UUID) (DataRecord, error) {
	record, exists := repo.Records[id]
	if !exists {
		return DataRecord{}, ErrRecordNotFound
	}
	return record, nil
}
