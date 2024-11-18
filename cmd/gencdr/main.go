package main

import (
	"fmt"
	"github.com/mezni/bridge/tools/gencdr"
	"time"
)

func main() {
	// Create a new list of records
	records := gencdr.NewRecordList()

	// Add records to the list
	records.AddRecord(gencdr.NewRecord("Name", "John Doe"))
	records.AddRecord(gencdr.NewRecord("Age", 30))
	records.AddRecord(gencdr.NewRecord("Birthday", time.Date(1994, time.January, 1, 0, 0, 0, 0, time.UTC)))
	records.AddRecord(gencdr.NewRecord("Occupation", "Software Engineer"))
	records.AddRecord(gencdr.NewRecord("Experience", 5))
	records.AddRecord(gencdr.NewRecord("Joining Date", time.Date(2020, time.January, 1, 0, 0, 0, 0, time.UTC)))

	// Print records
	for _, r := range records {
		fmt.Printf("%s: %v\n", r.Key, r.Value)
	}
}