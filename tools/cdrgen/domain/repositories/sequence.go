package repositories

import (
	"errors"
	"github.com/mezni/bridge/tools/cdrgen/domain/entities"
)

// SequenceRepository defines the contract for sequence storage.
type SequenceRepository interface {
	Add(sequence *entities.SequenceGenerator) error
	Get(name string) (*entities.SequenceGenerator, error)
	Remove(name string) error
}

var ErrSequenceNotFound = errors.New("sequence not found")
var ErrSequenceExists = errors.New("sequence already exists")
var ErrInvalidStep = errors.New("step should be positif int")
