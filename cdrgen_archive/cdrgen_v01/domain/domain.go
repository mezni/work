package domain

// Config represents the application configuration.
type Config struct {
	App struct {
		Version string `yaml:"version"`
	} `yaml:"app"`
}
