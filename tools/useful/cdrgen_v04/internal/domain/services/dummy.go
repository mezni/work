package services

import (
	"github.com/mezni/bridge/tools/cdrgen/internal/domain/interfaces"
)

// DummyService is a dummy service that does nothing but logs its actions
type DummyService struct {
	logger interfaces.Logger // Logger is injected into the service
}

// NewDummyService creates a new instance of DummyService with a logger
func NewDummyService(logger interfaces.Logger) *DummyService {
	return &DummyService{
		logger: logger,
	}
}

// DoNothing performs an action that does nothing and logs the event
func (s *DummyService) DoNothing() {
	s.logger.Debug("Enter", "service", "DummyService")
	s.logger.Debug("Exit", "service", "DummyService")
}
