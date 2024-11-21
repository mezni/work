package gencdr

import (
	"testing"
	"time"
)

func TestNewRecord(t *testing.T) {
	key := "id"
	value := 1
	record := NewRecord(key, value)

	if len(record) != 1 {
		t.Errorf("Expected record to have 1 key-value pair, but got %d", len(record))
	}

	if record[key] != value {
		t.Errorf("Expected record to have value %v for key %s, but got %v", value, key, record[key])
	}
}

func TestNewRecords(t *testing.T) {
	records := NewRecords()

	if len(records) != 0 {
		t.Errorf("Expected new records to be empty, but got %d records", len(records))
	}
}

func TestAddRecord(t *testing.T) {
	records := NewRecords()
	record := NewRecord("id", 1)

	records.AddRecord(record)

	if len(records) != 1 {
		t.Errorf("Expected records to have 1 record, but got %d", len(records))
	}

	if records[0]["id"] != 1 {
		t.Errorf("Expected record to have value 1 for key id, but got %v", records[0]["id"])
	}
}

func TestAddKeyValue(t *testing.T) {
	record := NewRecord("id", 1)
	key := "name"
	value := "John Doe"

	record.AddKeyValue(key, value)

	if len(record) != 2 {
		t.Errorf("Expected record to have 2 key-value pairs, but got %d", len(record))
	}

	if record[key] != value {
		t.Errorf("Expected record to have value %v for key %s, but got %v", value, key, record[key])
	}
}

func TestPrintRecords(t *testing.T) {
	records := NewRecords()
	record1 := NewRecord("id", 1)
	record1.AddKeyValue("name", "John Doe")
	records.AddRecord(record1)

	record2 := NewRecord("id", 2)
	record2.AddKeyValue("name", "Jane Doe")
	records.AddRecord(record2)

	// Test that PrintRecords doesn't panic
	records.PrintRecords()
}

func TestRecordWithDifferentTypes(t *testing.T) {
	record := NewRecord("id", 1)
	record.AddKeyValue("name", "John Doe")
	record.AddKeyValue("birthdate", time.Date(1990, time.January, 1, 0, 0, 0, 0, time.UTC))

	if len(record) != 3 {
		t.Errorf("Expected record to have 3 key-value pairs, but got %d", len(record))
	}

	if record["id"] != 1 {
		t.Errorf("Expected record to have value 1 for key id, but got %v", record["id"])
	}

	if record["name"] != "John Doe" {
		t.Errorf("Expected record to have value John Doe for key name, but got %v", record["name"])
	}

	if record["birthdate"].(time.Time).Year() != 1990 {
		t.Errorf("Expected record to have value 1990 for key birthdate, but got %v", record["birthdate"])
	}
}