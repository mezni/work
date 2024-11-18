package main

import (
//	"fmt"
	"github.com/mezni/bridge/tools/gencdr"
	"time"
)

func main() {
	// Create a new list of records
	records := gencdr.NewRecords()

	// Create some sample records
	record1 := gencdr.NewRecord("id", 1)
	record1.AddKeyValue("name", "John Doe")
	record1.AddKeyValue("birthdate", time.Date(1990, time.January, 1, 0, 0, 0, 0, time.UTC))
	record1.AddKeyValue("city", "Toronto")

	record2 := gencdr.NewRecord("id", 2)
	record2.AddKeyValue("name", "Jane Doe")
	record2.AddKeyValue("birthdate", time.Date(1995, time.June, 15, 0, 0, 0, 0, time.UTC))
	record2.AddKeyValue("city", "Vancouver")

	record3 := gencdr.NewRecord("id", 3)
	record3.AddKeyValue("name", "Bob Smith")
	record3.AddKeyValue("birthdate", time.Date(1980, time.March, 20, 0, 0, 0, 0, time.UTC))
	record3.AddKeyValue("city", "Montreal")

	// Add records to the list
	records.AddRecord(record1)
	records.AddRecord(record2)
	records.AddRecord(record3)

	// Print out all records
	records.PrintRecords()
}