package application

import (
	"fmt"
	"github.com/mezni/bridge/tools/cdrgen/internal/entities/entities"
)

// CallRecordService provides business logic for managing CallRecords.
type CallRecordService struct {
	repo entities.Repository
}

// NewCallRecordService creates and returns a new CallRecordService.
func NewCallRecordService(repo entities.Repository) *CallRecordService {
	return &CallRecordService{repo: repo}
}

// ListCallRecords lists all the CallRecords stored in the repository.
func (s *CallRecordService) ListCallRecords() {
	callRecords, err := s.repo.FindAll()
	if err != nil {
		fmt.Printf("Error retrieving call records: %v\n", err)
		return
	}

	// Output the call records as maps of key-value pairs
	for _, callRecord := range callRecords {
		fmt.Println(callRecord)
	}
}

// AddCallRecord adds a new CallRecord to the repository.
func (s *CallRecordService) AddCallRecord(callRecord entities.CallRecord) {
	err := s.repo.Save(callRecord)
	if err != nil {
		fmt.Printf("Error saving call record: %v\n", err)
		return
	}
	fmt.Println("Call record saved successfully!")
}
