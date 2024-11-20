package main

import (
    "fmt"
    "errors"
)

// Define CalldataMap as a new type for map[string]interface{}
type CalldataMap map[string]interface{}

// CalldataRecord struct with a CalldataMap field
type CalldataRecord struct {
    Record CalldataMap // Using CalldataMap instead of a direct map
}

// Define the error message formats as variables
var missingFieldErrorFormat = "required field '%s' is missing"
var noRecordsError = "no records available"

// Validate method checks if the required fields are present in the Record map
func (c *CalldataRecord) Validate(requiredFields []string) error {
    for _, field := range requiredFields {
        if _, exists := c.Record[field]; !exists {
            return errors.New(fmt.Sprintf(missingFieldErrorFormat, field))
        }
    }
    return nil
}

// NewCalldataRecord function to create a new CalldataRecord with provided data and validate it
func NewCalldataRecord(record CalldataMap, requiredFields []string) (*CalldataRecord, error) {
    // Create a new CalldataRecord instance with the provided record map
    newRecord := &CalldataRecord{
        Record: record,
    }

    // Perform validation on the created record
    if err := newRecord.Validate(requiredFields); err != nil {
        return nil, err // Return nil and the error if validation fails
    }

    return newRecord, nil // Return the new record if validation succeeds
}

// MemoryRepo struct to manage CalldataRecord entries in memory
type MemoryRepo struct {
    records []*CalldataRecord // Slice of pointers to CalldataRecord
}

// Add method to add a CalldataRecord to the repository
func (repo *MemoryRepo) Add(record *CalldataRecord) {
    repo.records = append(repo.records, record)
}

// GetLength method to return the number of records in the repository
func (repo *MemoryRepo) GetLength() int {
    return len(repo.records)
}

// GetAll method to return all CalldataRecords from the repository
func (repo *MemoryRepo) GetAll() ([]*CalldataRecord, error) {
    if len(repo.records) == 0 {
        return nil, errors.New(noRecordsError) // Use the variable for error message
    }

    return repo.records, nil
}

func main() {
    // Define the record data
    recordData1 := CalldataMap{
        "key1": "value1",
        "key2": 42,
    }

    recordData2 := CalldataMap{
        "key1": "value2",
        "key2": 100,
    }

    // List of required fields
    requiredFields := []string{"key1", "key2"}

    // Create a new CalldataRecord instance and validate it
    record1, err := NewCalldataRecord(recordData1, []string{"key1", "key2"})
    if err != nil {
        fmt.Println("Validation failed:", err)
        return
    }

    record2, err := NewCalldataRecord(recordData2, requiredFields)
    if err != nil {
        fmt.Println("Validation failed:", err)
        return
    }

    // Create a MemoryRepo instance
    repo := &MemoryRepo{}

    // Add records to the repository
    repo.Add(record1)
    repo.Add(record2)

    // Print the length of the repository
    fmt.Printf("Repo length: %d\n", repo.GetLength())

    // Get all entries from the repository
    allRecords, err := repo.GetAll()
    if err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("All records:")
        for _, record := range allRecords {
            fmt.Printf("%+v\n", record.Record) // Display each record
        }
    }
}
