package application

import (
	"fmt"
	"gopkg.in/yaml.v3"
	"os"
	"github.com/mezni/bridge/tools/cdrgen/domain"
)

// ConfigLoader is responsible for loading a configuration from a file.
type ConfigLoader struct {
	FilePath string
}

// Load parses the YAML file and returns a CmdConfig instance.
func (cl *ConfigLoader) Load() (*domain.CmdConfig, error) {
	file, err := os.Open(cl.FilePath)
	if err != nil {
		return nil, fmt.Errorf("error opening file: %w", err)
	}
	defer file.Close()

	var cmdConfig domain.CmdConfig
	decoder := yaml.NewDecoder(file)
	if err := decoder.Decode(&cmdConfig); err != nil {
		return nil, fmt.Errorf("error decoding YAML: %w", err)
	}

	return &cmdConfig, nil
}
