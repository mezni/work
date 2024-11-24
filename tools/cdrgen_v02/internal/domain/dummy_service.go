package domain

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/internal/application"
)

// DummyService represents a service that does nothing for demonstration
type DummyService struct {
	logger application.Logger
}

// NewDummyService creates a new instance of DummyService
func NewDummyService(logger application.Logger) *DummyService {
	return &DummyService{logger: logger}
}

// Start simulates starting the service (does nothing)
func (s *DummyService) Start(ctx context.Context, module string) {
	s.logger.Init(ctx, module).Info("DummyService started, doing nothing")
}

// Stop simulates stopping the service (does nothing)
func (s *DummyService) Stop(ctx context.Context, module string) {
	s.logger.Init(ctx, module).Info("DummyService stopped, doing nothing")
}
