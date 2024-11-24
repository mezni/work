package service

import (
	"github.com/mezni/bridge/tools/cdrgen/internal/domain"
	"github.com/mezni/bridge/tools/cdrgen/internal/infrastructure"
)

// SequenceService is responsible for orchestrating domain operations like
// generating sequences or validating them.
type SequenceService struct {
	repo   domain.SequenceRepositoryInterface
	logger infrastructure.Logger
}

// NewSequenceService creates a new SequenceService instance
func NewSequenceService(repo domain.SequenceRepositoryInterface, logger infrastructure.Logger) *SequenceService {
	return &SequenceService{repo: repo, logger: logger}
}

// GenerateSequence generates a sequence up to a given limit and stores it.
func (s *SequenceService) GenerateSequence(seq *domain.Sequence, limit int) ([]int, error) {
	if seq == nil {
		s.logger.Error("Sequence cannot be nil")
		return nil, domain.ErrSequenceCannotBeNil
	}

	var result []int
	for seq.Start <= limit {
		result = append(result, seq.Start)
		seq.Start += seq.Step
	}

	// Optionally add the sequence to the repository
	if err := s.repo.Add(*seq); err != nil {
		s.logger.Error("Error adding sequence to repository", "error", err)
		return nil, err
	}

	s.logger.Info("Generated sequence", "name", seq.Name)
	return result, nil
}
