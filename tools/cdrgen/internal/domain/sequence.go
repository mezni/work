package domain

import "errors"

// Sequence represents an Entity in the domain model.
type Sequence struct {
	Name  string
	Start int
	Step  int
}

// Error definitions specific to the Sequence entity
var (
	ErrInvalidStartValue   = errors.New("start value cannot be negative")
	ErrInvalidStepValue    = errors.New("step value must be greater than zero")
	ErrSequenceNotFound    = errors.New("sequence not found")
	ErrSequenceCannotBeNil = errors.New("sequence cannot be nil")
)

// NewSequence creates a new Sequence entity and ensures it is valid.
func NewSequence(name string, start, step int) (Sequence, error) {
	if start < 0 {
		return Sequence{}, ErrInvalidStartValue
	}
	if step <= 0 {
		return Sequence{}, ErrInvalidStepValue
	}

	return Sequence{
		Name:  name,
		Start: start,
		Step:  step,
	}, nil
}

// NextValue generates the next value based on the current state of the Sequence.
func (s *Sequence) NextValue() int {
	s.Start += s.Step
	return s.Start
}

// SequenceRepositoryInterface defines the contract for storing and retrieving Sequences.
type SequenceRepositoryInterface interface {
	// Add a new sequence to the repository
	Add(seq Sequence) error
	// Find retrieves a Sequence by name
	Find(name string) (Sequence, error)
	// GetAll retrieves all sequences in the repository
	GetAll() ([]Sequence, error)
}