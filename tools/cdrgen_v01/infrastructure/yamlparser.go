package infrastructure

import (
	"fmt"
	"os"
	"strings"
	"path/filepath"
	"github.com/mezni/bridge/tools/cdrgen/domain"
	"gopkg.in/yaml.v3"
)

// ParseYAMLConfig reads and parses the YAML configuration file.
func ParseYAMLConfig(filePath string) (*domain.Config, error) {
	if !isValidYAML(filePath) {
		return nil, fmt.Errorf("invalid file extension: %s. Only .yaml or .yml files are supported", filepath.Ext(filePath))
	}

	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to open config file: %w", err)
	}
	defer file.Close()

	var config domain.Config
	decoder := yaml.NewDecoder(file)
	if err := decoder.Decode(&config); err != nil {
		return nil, fmt.Errorf("failed to parse config file: %w", err)
	}

	return &config, nil
}

// isValidYAML checks if the file has a valid YAML extension (.yaml or .yml)
func isValidYAML(filePath string) bool {
	ext := strings.ToLower(filepath.Ext(filePath))
	return ext == ".yaml" || ext == ".yml"
}
