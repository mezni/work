package domain

import (
	"github.com/mezni/bridge/tools/cdrgen/infrastructure"
	"time"
)

// DummyService is a service that does nothing for the sake of illustration.
type DummyService struct {
	Logger *logger.Logger
}

// Start simulates starting the service and logging.
func (s *DummyService) Start() error {
	s.Logger.Info("DummyService started...")
	time.Sleep(3 * time.Second) // Simulate doing nothing
	s.Logger.Info("DummyService finished doing nothing.")
	return nil
}
