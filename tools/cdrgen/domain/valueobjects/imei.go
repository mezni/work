package valueobjects

import (
	"errors"
	"strconv"
)

type IMEI struct {
	value string
}

var (
	ErrInvalidIMEILength    = errors.New("invalid IMEI: must be 15 digits")
	ErrInvalidIMEICaracters = errors.New("invalid IMEI: must be numeric")
)

func NewIMEI(value string) (IMEI, error) {
	if len(value) != 15 {
		return IMEI{}, ErrInvalidIMEILength
	}
	_, err := strconv.Atoi(value)
	if err != nil {
		return IMEI{}, ErrInvalidIMEICaracters
	}
	return IMEI{value: value}, nil
}

func (i IMEI) String() string {
	return i.value
}
