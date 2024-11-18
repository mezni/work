package gencdr

import (
// "time"
)

// Record represents a key-value pair
type Record struct {
	Key   string
	Value interface{} // Value can be date, string or int
}

// NewRecord creates a new record
func NewRecord(key string, value interface{}) *Record {
	return &Record{
		Key:   key,
		Value: value,
	}
}

// RecordList represents a list of records
type RecordList []*Record

// NewRecordList creates a new list of records
func NewRecordList() RecordList {
	return make(RecordList, 0)
}

// AddRecord adds a record to the list
func (r *RecordList) AddRecord(record *Record) {
	*r = append(*r, record)
}
