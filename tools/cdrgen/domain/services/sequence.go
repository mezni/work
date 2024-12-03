package services

import (
	"context"
	"fmt"

	"github.com/mezni/bridge/tools/cdrgen/domain/entities"
	"github.com/mezni/bridge/tools/cdrgen/domain/repositories"
	"github.com/mezni/bridge/tools/cdrgen/infrastructure/logging"
)

type SequenceService struct {
	repo   repositories.SequenceRepository
	logger *logging.SlogLogger
}

// NewSequenceService creates a new SequenceService instance with logging.
func NewSequenceService(repo repositories.SequenceRepository, logger *logging.SlogLogger) *SequenceService {
	return &SequenceService{repo: repo, logger: logger}
}

// CreateSequence creates and adds a new SequenceGenerator to the repository.
func (s *SequenceService) CreateSequence(name string, initialValue, step int64) error {
	if step <= 0 {
		return repositories.ErrInvalidStep
	}

	s.logger.Debug(context.Background(), "Creating sequence", "name", name, "initialValue", initialValue, "step", step)

	sequence := entities.NewSequenceGenerator(name, initialValue, step)
	if err := s.repo.Add(sequence); err != nil {
		s.logger.Error(context.Background(), "Failed to add sequence to repository", "name", name, "error", err)
		return fmt.Errorf("service error: failed to add sequence: %w", err)
	}

	return nil
}

// GetNextValue retrieves the next value of a SequenceGenerator.
func (s *SequenceService) GetNextValue(name string) (int64, error) {
	sequence, err := s.repo.Get(name)
	if err != nil {
		s.logger.Error(context.Background(), "Failed to retrieve sequence", "name", name, "error", err)
		return 0, fmt.Errorf("service error: failed to retrieve sequence: %w", err)
	}

	return sequence.Next(), nil
}

// GetCurrentValue retrieves the current value of a SequenceGenerator.
func (s *SequenceService) GetCurrentValue(name string) (int64, error) {
	sequence, err := s.repo.Get(name)
	if err != nil {
		s.logger.Error(context.Background(), "Failed to retrieve current value", "name", name, "error", err)
		return 0, fmt.Errorf("service error: failed to retrieve current value: %w", err)
	}

	return sequence.Current(), nil
}

// ResetSequence resets a SequenceGenerator to a specified value.
func (s *SequenceService) ResetSequence(name string, value int64) error {
	sequence, err := s.repo.Get(name)
	if err != nil {
		s.logger.Error(context.Background(), "Failed to retrieve sequence for reset", "name", name, "error", err)
		return fmt.Errorf("service error: failed to retrieve sequence for reset: %w", err)
	}

	sequence.Reset(value)
	return nil
}
