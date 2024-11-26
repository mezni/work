package valueobjects

import (
	"errors"
	"strconv"
)

type IMSI struct {
	value string
}

var (
	ErrInvalidIMSILength    = errors.New("invalid IMSI: must be 15 digits")
	ErrInvalidIMSICaracters = errors.New("invalid IMSI: must be numeric")
)

func NewIMSI(value string) (IMSI, error) {
	// Validate IMSI format (e.g., length, numeric characters)
	if len(value) != 15 {
		return IMSI{}, ErrInvalidIMSILength
	}
	_, err := strconv.Atoi(value)
	if err != nil {
		return IMSI{}, ErrInvalidIMSICaracters
	}
	return IMSI{value: value}, nil
}

func (i IMSI) String() string {
	return i.value
}