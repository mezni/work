package persistance

import (
	"errors"
	"sync"

	"github.com/mezni/bridge/tools/cdrgen/internal/entities/entities"
)

// InMemoryRepository implements the Repository interface using an in-memory map.
type InMemoryRepository struct {
	data map[int]entities.CallRecord
	mu   sync.RWMutex // Ensures thread-safe operations
}

// NewInMemoryRepository creates and returns a new in-memory repository.
func NewInMemoryRepository() *InMemoryRepository {
	return &InMemoryRepository{
		data: make(map[int]entities.CallRecord),
	}
}

// FindAll returns all the CallRecords in the repository.
func (r *InMemoryRepository) FindAll() ([]entities.CallRecord, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	callRecords := make([]entities.CallRecord, 0, len(r.data))
	for _, callRecord := range r.data {
		callRecords = append(callRecords, callRecord)
	}
	return callRecords, nil
}

// FindByID retrieves a CallRecord by its ID.
func (r *InMemoryRepository) FindByID(id int) (entities.CallRecord, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	callRecord, exists := r.data[id]
	if !exists {
		return nil, errors.New("call record not found")
	}
	return callRecord, nil
}

// Save stores a CallRecord in the repository.
func (r *InMemoryRepository) Save(callRecord entities.CallRecord) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	id, ok := callRecord["id"].(float64) // JSON numbers are float64 by default
	if !ok {
		return errors.New("call record does not contain a valid 'id'")
	}

	r.data[int(id)] = callRecord
	return nil
}

// Delete removes a CallRecord by its ID.
func (r *InMemoryRepository) Delete(id int) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.data[id]; !exists {
		return errors.New("call record not found")
	}
	delete(r.data, id)
	return nil
}
