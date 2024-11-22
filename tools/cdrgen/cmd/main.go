package main

import (
	"github.com/mezni/bridge/tools/cdrgen/application"
	"github.com/mezni/bridge/tools/cdrgen/interfaces"
)

func main() {
	// Initialize the ConfigLoader with no file path yet
	loader := &application.ConfigLoader{}

	// Initialize the CommandLineHandler with the loader
	handler := interfaces.NewCommandLineHandler(loader)

	// Execute the command-line handler
	handler.Execute()
}
