package msisdn

import (
	"testing"
)

// TestNewMSISDNConfig tests the initialization of the MSISDNConfig struct
func TestNewMSISDNConfig(t *testing.T) {
	// Test case with default 6 digits
	config := NewMSISDNConfig([]string{"+1", "+44"})
	if len(config.prefixes) != 2 {
		t.Errorf("Expected 2 prefixes, got %d", len(config.prefixes))
	}
	if config.digits != 6 {
		t.Errorf("Expected 6 digits, got %d", config.digits)
	}
	if config.local {
		t.Error("Expected local to be false by default")
	}
}

// TestSetLocal tests the SetLocal method
func TestSetLocal(t *testing.T) {
	config := NewMSISDNConfig([]string{"+1"})
	config.SetLocal(true)
	if !config.local {
		t.Error("Expected local to be true")
	}
}

// TestGenerate tests the Generate method
func TestGenerate(t *testing.T) {
	config := NewMSISDNConfig([]string{"+1", "+44"})
	msisdn := config.Generate()
	if len(msisdn) <= 6 {
		t.Errorf("Generated MSISDN is too short: %s", msisdn)
	}
	if msisdn[0] != '+' {
		t.Error("Expected MSISDN to start with a '+' sign")
	}
}

// TestGenerateList tests the GenerateList method
func TestGenerateList(t *testing.T) {
	config := NewMSISDNConfig([]string{"+1", "+44"})
	msisdns := config.GenerateList(5)
	if len(msisdns) != 5 {
		t.Errorf("Expected 5 MSISDNs, got %d", len(msisdns))
	}
	for _, msisdn := range msisdns {
		if len(msisdn) <= 6 {
			t.Errorf("Generated MSISDN is too short: %s", msisdn)
		}
	}
}


