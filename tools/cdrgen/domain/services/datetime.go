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

	// Use RandomGenerator's NextInt64 to get a random offset
	duration := end.Unix() - start.Unix()
	randomOffset := g.randomGenerator.NextInt64(duration)

	return time.Unix(start.Unix()+randomOffset, 0).UTC(), nil
}

// FormatDatetime formats a datetime to the specified layout and time zone.
func (g *DatetimeGenerator) FormatDatetime(datetime time.Time, layout string, location *time.Location) string {
	if location != nil {
		datetime = datetime.In(location)
	}
	return datetime.Format(layout)
}
