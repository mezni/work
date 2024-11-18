package gencdr

import (
	"testing"
)

func TestNewRecord(t *testing.T) {
	key := "test_key"
	value := "test_value"
	record := NewRecord(key, value)

	if record.Key != key {
		t.Errorf("expected key %s, got %s", key, record.Key)
	}

	if record.Value != value {
		t.Errorf("expected value %s, got %s", value, record.Value)
	}
}

func TestNewRecordList(t *testing.T) {
	recordList := NewRecordList()
	if len(recordList) != 0 {
		t.Errorf("expected empty list, got %v", recordList)
	}
}

func TestAddRecord(t *testing.T) {
	recordList := NewRecordList()
	record := NewRecord("test_key", "test_value")
	recordList.AddRecord(record)

	if len(recordList) != 1 {
		t.Errorf("expected list with 1 record, got %v", recordList)
	}

	if recordList[0].Key != "test_key" {
		t.Errorf("expected key %s, got %s", "test_key", recordList[0].Key)
	}

	if recordList[0].Value != "test_value" {
		t.Errorf("expected value %s, got %s", "test_value", recordList[0].Value)
	}
}

func TestAddMultipleRecords(t *testing.T) {
	recordList := NewRecordList()
	record1 := NewRecord("test_key1", "test_value1")
	record2 := NewRecord("test_key2", "test_value2")
	recordList.AddRecord(record1)
	recordList.AddRecord(record2)

	if len(recordList) != 2 {
		t.Errorf("expected list with 2 records, got %v", recordList)
	}

	if recordList[0].Key != "test_key1" {
		t.Errorf("expected key %s, got %s", "test_key1", recordList[0].Key)
	}

	if recordList[1].Key != "test_key2" {
		t.Errorf("expected key %s, got %s", "test_key2", recordList[1].Key)
	}
}
