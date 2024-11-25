package services

import (
 "github.com/mezni/bridge/cdrgen/internal/domain/interfaces"
)

// DummyService is a dummy service that does nothing but logs its actions
type DummyService struct {
	logger logger.Logger // Logger added to the service
}

// NewDummyService creates a new instance of DummyService with a logger
func NewDummyService(logger logger.Logger) *DummyService {
	return &DummyService{
		logger: logger,
	}
}

// DoNothing performs an action that does nothing and logs the event
func (s *DummyService) DoNothing() {
	// Log that the service is doing nothing
	s.logger.Info("Dummy service is doing nothing...")

	// You can add additional log levels if needed
	s.logger.Debug("Debug log for DoNothing executed.")
}
