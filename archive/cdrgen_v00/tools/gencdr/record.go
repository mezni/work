package gencdr

import (
	"fmt"
)

// Record represents a single record with key-value pairs
type Record map[string]interface{}

// Records is a list of records
type Records []Record

// NewRecord creates a new record with a single key-value pair
func NewRecord(key string, value interface{}) Record {
	return Record{
		key: value,
	}
}

// NewRecords creates a new list of records
func NewRecords() Records {
	return make(Records, 0)
}

// AddRecord adds a record to the list of records
func (r *Records) AddRecord(record Record) {
	*r = append(*r, record)
}

// AddKeyValue adds a key-value pair to an existing record
func (r Record) AddKeyValue(key string, value interface{}) {
	r[key] = value
}

// PrintRecords prints out all records in the list
func (r Records) PrintRecords() {
	for i, record := range r {
		for key, value := range record {
			fmt.Printf("Record %d: %s: %v\n", i+1, key, value)
		}
		fmt.Println()
	}
}