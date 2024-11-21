package main

import (
	"errors"
	"fmt"
	"sync"
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

// CalldataRecordRepo interface defines methods for managing CalldataRecord objects
type CalldataRecordRepo interface {
	Add(record *CalldataRecord)         // Add a new record
	GetLength() int                     // Get the number of records in the repo
	GetAll() ([]*CalldataRecord, error) // Get all records from the repo
}

// MemoryRepo struct to manage CalldataRecord entries in memory with a Mutex for concurrency safety
type MemoryRepo struct {
	records []*CalldataRecord // Slice of pointers to CalldataRecord
	mu      sync.Mutex        // Mutex to ensure thread-safety
}

// Add method to add a CalldataRecord to the repository
func (repo *MemoryRepo) Add(record *CalldataRecord) {
	repo.mu.Lock()         // Lock before modifying the records
	defer repo.mu.Unlock() // Ensure the lock is released after the method completes

	repo.records = append(repo.records, record)
}

// GetLength method to return the number of records in the repository
func (repo *MemoryRepo) GetLength() int {
	repo.mu.Lock()         // Lock before accessing the records
	defer repo.mu.Unlock() // Ensure the lock is released after the method completes

	return len(repo.records)
}

// GetAll method to return all CalldataRecords from the repository
func (repo *MemoryRepo) GetAll() ([]*CalldataRecord, error) {
	repo.mu.Lock()         // Lock before accessing the records
	defer repo.mu.Unlock() // Ensure the lock is released after the method completes

	if len(repo.records) == 0 {
		return nil, errors.New(noRecordsError) // Use the variable for error message
	}

	return repo.records, nil
}

// CalldataService struct defines the service for managing records
type CalldataService struct {
	repo CalldataRecordRepo // The repository that the service will interact with
}

// NewCalldataService function to initialize a new service with the given repository and configurations
func NewCalldataService(repo CalldataRecordRepo, cfgs ...CalldataConfiguration) *CalldataService {
	service := &CalldataService{
		repo: repo,
	}

	// Apply each configuration function to the service
	for _, cfg := range cfgs {
		if err := cfg(service); err != nil {
			fmt.Printf("Error applying configuration: %v\n", err)
		}
	}

	return service
}

// AddRecord method to add a CalldataRecord to the repository
func (service *CalldataService) AddRecord(record *CalldataRecord) {
	service.repo.Add(record) // Delegate adding to the repository
}

// GetRecordCount method to get the count of records in the repository
func (service *CalldataService) GetRecordCount() int {
	return service.repo.GetLength() // Delegate counting to the repository
}

// GetAllRecords method to get all records from the repository
func (service *CalldataService) GetAllRecords() ([]*CalldataRecord, error) {
	return service.repo.GetAll() // Delegate fetching all records to the repository
}

// CalldataConfiguration type defines a function that modifies the CalldataService
type CalldataConfiguration func(os *CalldataService) error

// Example Configuration Function: A function to set some configuration on the CalldataService
func SetRecordLimit(limit int) CalldataConfiguration {
	return func(os *CalldataService) error {
		// This is an example, you could use this to apply a configuration on your service
		if limit < 0 {
			return errors.New("record limit cannot be negative")
		}
		fmt.Printf("Setting record limit to: %d\n", limit)
		return nil
	}
}

// Another Example Configuration Function: Enable Logging
func EnableLogging(enable bool) CalldataConfiguration {
	return func(os *CalldataService) error {
		if enable {
			fmt.Println("Logging is enabled.")
		} else {
			fmt.Println("Logging is disabled.")
		}
		return nil
	}
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

	// Create a MemoryRepo instance and assign it to the CalldataRecordRepo interface
	repo := &MemoryRepo{}

	// Create a CalldataService instance with the repo and configuration functions
	service := NewCalldataService(repo, SetRecordLimit(100), EnableLogging(true))

	// Add records to the service, which will interact with the repo
	service.AddRecord(record1)
	service.AddRecord(record2)

	// Print the length of the repository via the service
	fmt.Printf("Repo length: %d\n", service.GetRecordCount())

	// Get all entries from the service
	allRecords, err := service.GetAllRecords()
	if err != nil {
		fmt.Println("Error:", err)
	} else {
		fmt.Println("All records:")
		for _, record := range allRecords {
			fmt.Printf("%+v\n", record.Record) // Display each record
		}
	}
}
