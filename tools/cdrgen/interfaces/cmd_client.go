package interfaces

import (
	"flag"
	"fmt"
	"github.com/mezni/bridge/tools/cdrgen/application"
	"github.com/mezni/bridge/tools/cdrgen/domain"
)

// CommandLineHandler is responsible for managing the CLI input.
type CommandLineHandler struct {
	loader *application.ConfigLoader
}

// NewCommandLineHandler initializes a new CommandLineHandler.
func NewCommandLineHandler(loader *application.ConfigLoader) *CommandLineHandler {
	return &CommandLineHandler{loader: loader}
}

// Execute is the entry point for processing the CLI commands.
func (cli *CommandLineHandler) Execute() {
	// Define flags
	inputFile := flag.String("input_file", "", "Path to the input YAML file")
	verbose := flag.Bool("verbose", false, "Enable verbose output")
	help := flag.Bool("help", false, "Display help message")
	versionFlag := flag.Bool("version", false, "Display the version of the program")

	// Parse the command-line flags
	flag.Parse()

	// Display version if requested
	if *versionFlag {
		cli.showVersion()
		return
	}

	// Display help if requested
	if *help {
		cli.showHelp()
		return
	}

	// Ensure input file is provided
	if *inputFile == "" {
		fmt.Println("Error: You must provide an input YAML file.")
		cli.showHelp()
		return
	}

	// Set the file path in the loader
	cli.loader.FilePath = *inputFile

	// Load the config
	cmdConfig, err := cli.loader.Load()
	if err != nil {
		fmt.Println("Error loading configuration:", err)
		return
	}

	// Handle verbose output
	if *verbose {
		fmt.Println("Verbose mode is enabled.")
	}

	// Print the YAML content
	cli.printConfig(cmdConfig)
}

func (cli *CommandLineHandler) showHelp() {
	fmt.Println("Usage: go run main.go -input_file <input_file.yaml> -verbose")
	flag.PrintDefaults()
}

func (cli *CommandLineHandler) showVersion() {
	const version = "1.0.0"
	fmt.Println("Program Version:", version)
}

func (cli *CommandLineHandler) printConfig(cmdConfig *domain.CmdConfig) {
	fmt.Printf("YAML File Content:\nFileName: %s\n", cmdConfig.FileName)
}
