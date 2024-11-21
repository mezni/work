package main

import (
	"encoding/csv"
	"errors"
	"fmt"
	"os"
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

// CSVRepo struct implements CalldataRecordRepo and writes records to a CSV file
type CSVRepo struct {
	filepath string         // Path to the CSV file
	mu       sync.Mutex     // Mutex for thread-safety
}

// NewCSVRepo creates a new CSVRepo instance with the given file path
func NewCSVRepo(filepath string) *CSVRepo {
	return &CSVRepo{
		filepath: filepath,
	}
}

// Add method writes a new record to the CSV file
func (repo *CSVRepo) Add(record *CalldataRecord) {
	repo.mu.Lock()         // Lock before modifying the file
	defer repo.mu.Unlock() // Ensure the lock is released after the method completes

	// Open the file for appending or create it if it doesn't exist
	file, err := os.OpenFile(repo.filepath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)

	// Convert the CalldataRecord to a slice of strings for writing to the CSV
	var recordSlice []string
	for _, value := range record.Record {
		recordSlice = append(recordSlice, fmt.Sprintf("%v", value)) // Convert each field to string
	}

	// Write the record to the CSV
	if err := writer.Write(recordSlice); err != nil {
		fmt.Println("Error writing to CSV:", err)
		return
	}
	writer.Flush() // Ensure all data is written to the file
}

// GetLength method returns the number of records in the CSV file
func (repo *CSVRepo) GetLength() int {
	repo.mu.Lock()
	defer repo.mu.Unlock()

	// Open the file for reading
	file, err := os.Open(repo.filepath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return 0
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		fmt.Println("Error reading CSV:", err)
		return 0
	}

	return len(records)
}

// GetAll method returns all CalldataRecords from the CSV file
func (repo *CSVRepo) GetAll() ([]*CalldataRecord, error) {
	repo.mu.Lock()
	defer repo.mu.Unlock()

	// Open the file for reading
	file, err := os.Open(repo.filepath)
	if err != nil {
		return nil, fmt.Errorf("error opening file: %v", err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, fmt.Errorf("error reading CSV: %v", err)
	}

	// Convert CSV rows into CalldataRecord objects
	var calldataRecords []*CalldataRecord
	for _, record := range records {
		calldataRecord := &CalldataRecord{
			Record: make(CalldataMap),
		}
		for i, value := range record {
			calldataRecord.Record[fmt.Sprintf("field%d", i+1)] = value
		}
		calldataRecords = append(calldataRecords, calldataRecord)
	}

	if len(calldataRecords) == 0 {
		return nil, errors.New(noRecordsError)
	}

	return calldataRecords, nil
}

// CalldataService struct defines the service for managing records
type CalldataService struct {
	repo CalldataRecordRepo // The repository that the service will interact with
}

// NewCalldataService function to initialize a new service with the given repository
func NewCalldataService(repo CalldataRecordRepo) *CalldataService {
	return &CalldataService{
		repo: repo,
	}
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
	record1, err := NewCalldataRecord(recordData1, requiredFields)
	if err != nil {
		fmt.Println("Validation failed:", err)
		return
	}

	record2, err := NewCalldataRecord(recordData2, requiredFields)
	if err != nil {
		fmt.Println("Validation failed:", err)
		return
	}

	// Create a CSVRepo instance and assign it to the CalldataRecordRepo interface
	repo := NewCSVRepo("records.csv")

	// Create a CalldataService instance with the repo
	service := NewCalldataService(repo)

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
