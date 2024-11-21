package gencdr

import (
	"testing"
)

func TestNewSequence(t *testing.T) {
	seq := NewSequence("test", 1, 1)
	if seq.Name != "test" {
		t.Errorf("expected Name to be 'test', got '%s'", seq.Name)
	}
	if seq.Start != 1 {
		t.Errorf("expected Start to be 1, got %d", seq.Start)
	}
	if seq.Step != 1 {
		t.Errorf("expected Step to be 1, got %d", seq.Step)
	}
	if seq.curr != 1 {
		t.Errorf("expected curr to be 1, got %d", seq.curr)
	}
}

func TestSequenceNext(t *testing.T) {
	seq := NewSequence("test", 1, 1)
	if seq.Next() != 1 {
		t.Errorf("expected Next to return 1, got %d", seq.Next())
	}
	if seq.Next() != 2 {
		t.Errorf("expected Next to return 2, got %d", seq.Next())
	}
}

func TestSequenceReset(t *testing.T) {
	seq := NewSequence("test", 1, 1)
	seq.Next()
	seq.Reset()
	if seq.Next() != 1 {
		t.Errorf("expected Next to return 1 after Reset, got %d", seq.Next())
	}
}

func TestNewSequenceManager(t *testing.T) {
	sm := NewSequenceManager()
	if len(sm.sequences) != 0 {
		t.Errorf("expected sequences to be empty, got %v", sm.sequences)
	}
}

func TestSequenceManagerAddSequence(t *testing.T) {
	sm := NewSequenceManager()
	sm.AddSequence("test", 1, 1)
	if len(sm.sequences) != 1 {
		t.Errorf("expected 1 sequence, got %d", len(sm.sequences))
	}
}

func TestSequenceManagerGetNext(t *testing.T) {
	sm := NewSequenceManager()
	sm.AddSequence("test", 1, 1)
	value, err := sm.GetNext("test")
	if err != nil {
		t.Errorf("expected no error, got %v", err)
	}
	if value != 1 {
		t.Errorf("expected value to be 1, got %d", value)
	}
}

func TestSequenceManagerGetNextUnknownSequence(t *testing.T) {
	sm := NewSequenceManager()
	_, err := sm.GetNext("unknown")
	if err == nil {
		t.Errorf("expected error, got nil")
	}
}

func TestSequenceManagerReset(t *testing.T) {
	sm := NewSequenceManager()
	sm.AddSequence("test", 1, 1)
	sm.GetNext("test")
	sm.Reset("test")
	value, err := sm.GetNext("test")
	if err != nil {
		t.Errorf("expected no error, got %v", err)
	}
	if value != 1 {
		t.Errorf("expected value to be 1 after Reset, got %d", value)
	}
}

func TestSequenceManagerResetUnknownSequence(t *testing.T) {
	sm := NewSequenceManager()
	err := sm.Reset("unknown")
	if err == nil {
		t.Errorf("expected error, got nil")
	}
}

func TestSequenceManagerRemoveSequence(t *testing.T) {
	sm := NewSequenceManager()
	sm.AddSequence("test", 1, 1)
	err := sm.RemoveSequence("test")
	if err != nil {
		t.Errorf("expected no error, got %v", err)
	}
	if len(sm.sequences) != 0 {
		t.Errorf("expected sequences to be empty, got %d", len(sm.sequences))
	}
}

func TestSequenceManagerRemoveUnknownSequence(t *testing.T) {
	sm := NewSequenceManager()
	err := sm.RemoveSequence("unknown")
	if err == nil {
		t.Errorf("expected error, got nil")
	}
}

func TestSequenceManagerListSequences(t *testing.T) {
	sm := NewSequenceManager()
	sm.AddSequence("test1", 1, 1)
	sm.AddSequence("test2", 1, 1)
	sequences := sm.ListSequences()
	if len(sequences) != 2 {
		t.Errorf("expected 2 sequences, got %d", len(sequences))
	}
}