package valueobjects

import (
	"errors"
	"strconv"
)

var (
	ErrInvalidIMSILength = errors.New("invalid IMSI: must be 15 digits")
)

type IMSI struct {
	value string
}

func NewIMSI(value string) (IMSI, error) {
	if len(value) != 15 {
		return IMSI{}, ErrInvalidIMSILength
	}

	if _, err := strconv.Atoi(value); err != nil {
		return IMSI{}, ErrInvalidIMSILength
	}

	return IMSI{value: value}, nil
}

func (i IMSI) String() string {
	return i.value
}
