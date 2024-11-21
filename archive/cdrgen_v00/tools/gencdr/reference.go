package gencdr

import (
	"errors"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// Custom error types
var (
	ErrTableNotFound = errors.New("table not found")
	ErrInvalidIndex  = errors.New("invalid row index")
	ErrTableEmpty    = errors.New("table is empty")
)

// ReferenceRow represents a row in the table
type ReferenceRow map[string]interface{}

// ReferenceTable represents a table with rows
type ReferenceTable struct {
	Name       string
	References []ReferenceRow
	mu         sync.RWMutex
}

// ReferenceRepo represents a repository of tables
type ReferenceRepo struct {
	References map[string]*ReferenceTable
	mu         sync.RWMutex
}

// NewReferenceTable creates a new table
func NewReferenceTable(name string) *ReferenceTable {
	return &ReferenceTable{
		Name:       name,
		References: make([]ReferenceRow, 0),
	}
}

// NewReferenceRepo creates a new repository
func NewReferenceRepo() *ReferenceRepo {
	return &ReferenceRepo{
		References: make(map[string]*ReferenceTable),
	}
}

// AddTable adds a table to the repository
func (r *ReferenceRepo) AddTable(table *ReferenceTable) {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.References[table.Name] = table
}

// RemoveTable removes a table from the repository
func (r *ReferenceRepo) RemoveTable(name string) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	if _, ok := r.References[name]; !ok {
		return ErrTableNotFound
	}
	delete(r.References, name)
	return nil
}

// GetTable retrieves a table from the repository
func (r *ReferenceRepo) GetTable(name string) (*ReferenceTable, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	table, ok := r.References[name]
	if !ok {
		return nil, ErrTableNotFound
	}
	return table, nil
}

// UpdateTable updates a table in the repository
func (r *ReferenceRepo) UpdateTable(name string, table *ReferenceTable) {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.References[name] = table
}

// AddRow adds a row to the table
func (r *ReferenceTable) AddRow(row ReferenceRow) {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.References = append(r.References, row)
}

// RemoveRow removes a row from the table
func (r *ReferenceTable) RemoveRow(index int) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	if index < 0 || index >= len(r.References) {
		return ErrInvalidIndex
	}
	r.References = append(r.References[:index], r.References[index+1:]...)
	return nil
}

// GetRow retrieves a row from the table
func (r *ReferenceTable) GetRow(index int) (ReferenceRow, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	if index < 0 || index >= len(r.References) {
		return nil, ErrInvalidIndex
	}
	return r.References[index], nil
}

// UpdateRow updates a row in the table
func (r *ReferenceTable) UpdateRow(index int, row ReferenceRow) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	if index < 0 || index >= len(r.References) {
		return ErrInvalidIndex
	}
	r.References[index] = row
	return nil
}

// ClearRows clears all rows from the table
func (r *ReferenceTable) ClearRows() {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.References = make([]ReferenceRow, 0)
}

// GetTableLength returns the number of rows in the table
func (r *ReferenceTable) GetTableLength() int {
	r.mu.RLock()
	defer r.mu.RUnlock()
	return len(r.References)
}

// GetRandomRow returns a random row from the table
func (r *ReferenceTable) GetRandomRow() (ReferenceRow, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	if len(r.References) == 0 {
		return nil, ErrTableEmpty
	}

	rand.Seed(time.Now().UnixNano())
	index := rand.Intn(len(r.References))

	return r.References[index], nil
}