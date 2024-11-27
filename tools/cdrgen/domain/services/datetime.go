package services

import (
	"errors"
	"time"
)

var ErrInvalidDateRange = errors.New("invalid date range: start date must be before end date")

type DatetimeGenerator struct {
	randomGenerator *RandomGenerator
}

func NewDatetimeGenerator() *DatetimeGenerator {
	return &DatetimeGenerator{randomGenerator: NewRandomGenerator()}
}

// GenerateRandomDatetime generates a random datetime within the specified range.
func (g *DatetimeGenerator) GenerateRandomDatetime(start, end time.Time) (time.Time, error) {
	if start.After(end) {
		return time.Time{}, ErrInvalidDateRange
	}

	// Calculate the range in seconds
	duration := end.Unix() - start.Unix()
	if duration < 0 {
		return time.Time{}, ErrInvalidDateRange
	}

	// Generate a random offset
	randomOffset := g.randomGenerator.randSource.Int63n(duration)
	return time.Unix(start.Unix()+randomOffset, 0).UTC(), nil
}

// FormatDatetime formats a datetime to the specified layout and time zone.
func (g *DatetimeGenerator) FormatDatetime(datetime time.Time, layout string, location *time.Location) string {
	if location != nil {
		datetime = datetime.In(location)
	}
	return datetime.Format(layout)
}
