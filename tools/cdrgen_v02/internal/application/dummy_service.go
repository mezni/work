package application

import (
	"context"
	"github.com/mezni/bridge/tools/cdrgen/internal/domain"
)

// ApplicationService defines methods for business logic handling
type ApplicationService struct {
	dummyService *domain.DummyService
	logger       Logger
}

// NewApplicationService creates a new ApplicationService
func NewApplicationService(dummyService *domain.DummyService, logger Logger) *ApplicationService {
	return &ApplicationService{
		dummyService: dummyService,
		logger:       logger,
	}
}

// StartService starts the dummy service and logs the activity
func (s *ApplicationService) StartService(ctx context.Context, module string) {
	s.logger.Init(ctx, module).Info("Starting DummyService")
	s.dummyService.Start(ctx, module)
}

// StopService stops the dummy service and logs the activity
func (s *ApplicationService) StopService(ctx context.Context, module string) {
	s.logger.Init(ctx, module).Info("Stopping DummyService")
	s.dummyService.Stop(ctx, module)
}
