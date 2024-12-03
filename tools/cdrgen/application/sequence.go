package application

import (
	"context"
	"fmt"

	"github.com/mezni/bridge/tools/cdrgen/domain/services"
	"github.com/mezni/bridge/tools/cdrgen/infrastructure/logging"
)

type SequenceApplication struct {
	service *services.SequenceService
	logger  *logging.SlogLogger
}

// NewSequenceApplication creates a new instance of SequenceApplication with logging.
func NewSequenceApplication(service *services.SequenceService, logger *logging.SlogLogger) *SequenceApplication {
	return &SequenceApplication{service: service, logger: logger}
}

// CreateSequence handles the use case for creating a sequence.
func (app *SequenceApplication) CreateSequence(ctx context.Context, name string, initialValue, step int64) error {
	app.logger.Info(ctx, "Creating sequence", "name", name, "initialValue", initialValue, "step", step)

	err := app.service.CreateSequence(name, initialValue, step)
	if err != nil {
		app.logger.Error(ctx, "Failed to create sequence", "name", name, "error", err)
		return fmt.Errorf("application error: failed to create sequence: %w", err)
	}

	app.logger.Info(ctx, "Sequence created successfully", "name", name)
	return nil
}

// GenerateNextValue generates the next value for the given sequence.
func (app *SequenceApplication) GenerateNextValue(ctx context.Context, name string) (int64, error) {
	app.logger.Info(ctx, "Generating next value for sequence", "name", name)

	value, err := app.service.GetNextValue(name)
	if err != nil {
		app.logger.Error(ctx, "Failed to generate next value", "name", name, "error", err)
		return 0, fmt.Errorf("application error: failed to generate next value: %w", err)
	}

	app.logger.Info(ctx, "Next value generated successfully", "name", name, "value", value)
	return value, nil
}

// GetSequenceCurrentValue retrieves the current value of the sequence.
func (app *SequenceApplication) GetSequenceCurrentValue(ctx context.Context, name string) (int64, error) {
	app.logger.Info(ctx, "Retrieving current value for sequence", "name", name)

	value, err := app.service.GetCurrentValue(name)
	if err != nil {
		app.logger.Error(ctx, "Failed to retrieve current value", "name", name, "error", err)
		return 0, fmt.Errorf("application error: failed to retrieve current value: %w", err)
	}

	app.logger.Info(ctx, "Current value retrieved successfully", "name", name, "value", value)
	return value, nil
}

// ResetSequence resets the sequence to a specific value.
func (app *SequenceApplication) ResetSequence(ctx context.Context, name string, value int64) error {
	app.logger.Info(ctx, "Resetting sequence", "name", name, "value", value)

	err := app.service.ResetSequence(name, value)
	if err != nil {
		app.logger.Error(ctx, "Failed to reset sequence", "name", name, "error", err)
		return fmt.Errorf("application error: failed to reset sequence: %w", err)
	}

	app.logger.Info(ctx, "Sequence reset successfully", "name", name)
	return nil
}
