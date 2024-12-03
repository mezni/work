package inmemory

import (
	"github.com/mezni/bridge/tools/cdrgen/domain/entities"
	"github.com/mezni/bridge/tools/cdrgen/domain/repositories"
	"sync"
)

// InMemorySequenceRepository is an in-memory implementation of SequenceRepository.
type InMemorySequenceRepository struct {
	mu        sync.Mutex
	sequences map[string]*entities.SequenceGenerator
}

// NewInMemorySequenceRepository creates a new InMemorySequenceRepository instance.
func NewInMemorySequenceRepository() *InMemorySequenceRepository {
	return &InMemorySequenceRepository{
		sequences: make(map[string]*entities.SequenceGenerator),
	}
}

// Add adds a new SequenceGenerator to the repository.
func (r *InMemorySequenceRepository) Add(sequence *entities.SequenceGenerator) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.sequences[sequence.Name()]; exists {
		return repositories.ErrSequenceExists
	}

	r.sequences[sequence.Name()] = sequence
	return nil
}

// Get retrieves a SequenceGenerator by its name.
func (r *InMemorySequenceRepository) Get(name string) (*entities.SequenceGenerator, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	sequence, exists := r.sequences[name]
	if !exists {
		return nil, repositories.ErrSequenceNotFound
	}

	return sequence, nil
}

// Remove deletes a SequenceGenerator from the repository.
func (r *InMemorySequenceRepository) Remove(name string) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.sequences[name]; !exists {
		return repositories.ErrSequenceNotFound
	}

	delete(r.sequences, name)
	return nil
}
