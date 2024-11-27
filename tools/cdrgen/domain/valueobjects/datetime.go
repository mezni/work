package valueobjects

import (
	"errors"
	"time"
)

var ErrInvalidDatetime = errors.New("invalid datetime: must not be zero")

type Datetime struct {
	value time.Time
}

func NewDatetime(value time.Time) (Datetime, error) {
	if value.IsZero() {
		return Datetime{}, ErrInvalidDatetime
	}
	return Datetime{value: value}, nil
}

func (d Datetime) String() string {
	return d.value.Format(time.RFC3339)
}

func (d Datetime) Format(layout string) string {
	return d.value.Format(layout)
}
