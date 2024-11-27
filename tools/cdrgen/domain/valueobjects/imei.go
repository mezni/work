package valueobjects

import (
	"errors"
	"strconv"
)

var (
	ErrInvalidIMEILength = errors.New("invalid IMEI: must be 15 digits")
)

type IMEI struct {
	value string
}

func NewIMEI(value string) (IMEI, error) {
	if len(value) != 15 {
		return IMEI{}, ErrInvalidIMEILength
	}

	if _, err := strconv.Atoi(value); err != nil {
		return IMEI{}, ErrInvalidIMEILength
	}

	return IMEI{value: value}, nil
}

func (i IMEI) String() string {
	return i.value
}
