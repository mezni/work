package main

import (
	"fmt"
	"gopkg.in/yaml.v3"
	"io/ioutil"
)

type Config struct {
	FilenamePattern string `yaml:"filename_pattern"`
}

func LoadConfig(filename string) (Config, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return Config{}, err
	}

	var config Config
	err = yaml.Unmarshal(data, &config)
	return config, err
}

func main() {
	config, err := LoadConfig("config.yaml")
	if err != nil {
		fmt.Println("Error loading config:", err)
		return
	}

	// Generate a filename based on the loaded pattern
	//	filename := GenerateFilename(config.FilenamePattern)
	if config.FilenamePattern == "" {
		config.FilenamePattern = "default_{YYYY}{MM}{DD}.txt"
	}
	fmt.Println(config.FilenamePattern)
}
