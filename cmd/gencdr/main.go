package main

import (
//	"fmt"
	"github.com/mezni/bridge/tools/gencdr"
//	"time"
)

func main() {
	// Create a new list of records
	records := gencdr.NewRecords()

	// Create some sample records
	record1 := gencdr.NewRecord("id", 1)
	record1.AddKeyValue("cdr_id", 1111)


	// Add records to the list
	records.AddRecord(record1)


	// Print out all records
	records.PrintRecords()
}