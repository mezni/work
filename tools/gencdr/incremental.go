package gencdr

import (
	"fmt"
	"sync"
)

// Sequence represents a single sequence generator
type Sequence struct {
	Name  string
	Start int
	Step  int
	curr  int
	mu    sync.Mutex
}

// NewSequence initializes a new Sequence
func NewSequence(name string, start, step int) *Sequence {
	return &Sequence{
		Name:  name,
		Start: start,
		Step:  step,
		curr:  start,
	}
}

// Next generates the next value in the sequence
func (s *Sequence) Next() int {
	s.mu.Lock()
	defer s.mu.Unlock()
	value := s.curr
	s.curr += s.Step
	return value
}

// Reset resets the sequence to its starting value
func (s *Sequence) Reset() {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.curr = s.Start
}

// SequenceManager manages a collection of sequences
type SequenceManager struct {
	sequences map[string]*Sequence
	mu        sync.Mutex
}

// NewSequenceManager initializes a new SequenceManager
func NewSequenceManager() *SequenceManager {
	return &SequenceManager{
		sequences: make(map[string]*Sequence),
	}
}

// AddSequence adds a new sequence to the manager
func (sm *SequenceManager) AddSequence(name string, start, step int) {
	sm.mu.Lock()
	defer sm.mu.Unlock()
	sm.sequences[name] = NewSequence(name, start, step)
}

// GetNext generates the next value for a given sequence by name
func (sm *SequenceManager) GetNext(name string) (int, error) {
	sm.mu.Lock()
	defer sm.mu.Unlock()
	seq, exists := sm.sequences[name]
	if !exists {
		return 0, fmt.Errorf("sequence %q not found", name)
	}
	return seq.Next(), nil
}

// Reset resets a specific sequence by name
func (sm *SequenceManager) Reset(name string) error {
	sm.mu.Lock()
	defer sm.mu.Unlock()
	seq, exists := sm.sequences[name]
	if !exists {
		return fmt.Errorf("sequence %q not found", name)
	}
	seq.Reset()
	return nil
}

// RemoveSequence removes a sequence by name
func (sm *SequenceManager) RemoveSequence(name string) error {
	sm.mu.Lock()
	defer sm.mu.Unlock()
	if _, exists := sm.sequences[name]; !exists {
		return fmt.Errorf("sequence %q not found", name)
	}
	delete(sm.sequences, name)
	return nil
}

// ListSequences lists all sequence names
func (sm *SequenceManager) ListSequences() []string {
	sm.mu.Lock()
	defer sm.mu.Unlock()
	names := make([]string, 0, len(sm.sequences))
	for name := range sm.sequences {
		names = append(names, name)
	}
	return names
}
