package infrastructure

import (
	"fmt"
	"github.com/mezni/bridge/tools/cdrgen/internal/domain"
	"sync"
)

// SequenceRepository is an implementation of SequenceRepositoryInterface
// with concurrency control using a Mutex.
type SequenceRepository struct {
	sequences map[string]domain.Sequence
	mu        sync.Mutex // Mutex to ensure thread-safe access
}

// NewSequenceRepository creates a new SequenceRepository
func NewSequenceRepository() *SequenceRepository {
	return &SequenceRepository{sequences: make(map[string]domain.Sequence)}
}

// Add stores a sequence in the repository.
func (r *SequenceRepository) Add(seq domain.Sequence) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.sequences[seq.Name]; exists {
		return fmt.Errorf("sequence with name %s already exists", seq.Name)
	}

	r.sequences[seq.Name] = seq
	return nil
}

// Find retrieves a sequence by name from the repository.
func (r *SequenceRepository) Find(name string) (domain.Sequence, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	seq, exists := r.sequences[name]
	if !exists {
		return domain.Sequence{}, domain.ErrSequenceNotFound
	}

	return seq, nil
}

// GetAll retrieves all sequences in the repository.
func (r *SequenceRepository) GetAll() ([]domain.Sequence, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	// Create a slice to return all sequences
	var allSequences []domain.Sequence
	for _, seq := range r.sequences {
		allSequences = append(allSequences, seq)
	}

	return allSequences, nil
}
