package services

import "github.com/mezni/bridge/cdrgen/internal/application/interfaces"

// DummyService does nothing, just demonstrates how logging is injected
type DummyService struct {
    logger logger.Logger
}

// NewDummyService creates a new instance of DummyService with a logger
func NewDummyService(l logger.Logger) *DummyService {
    return &DummyService{
        logger: l,
    }
}

// DoSomething demonstrates how the service might use the logger
func (s *DummyService) DoSomething() {
    s.logger.Info("Dummy service doing nothing...")
}
