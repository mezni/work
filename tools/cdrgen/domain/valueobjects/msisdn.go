package valueobjects

import (
	"errors"
	"strconv"
)

var ErrInvalidMSISDN = errors.New("invalid MSISDN: must be numeric and between 10 and 15 digits")

type MSISDN struct {
	value string
}

func NewMSISDN(value string) (MSISDN, error) {
	if len(value) < 10 || len(value) > 15 {
		return MSISDN{}, ErrInvalidMSISDN
	}

	if _, err := strconv.Atoi(value); err != nil {
		return MSISDN{}, ErrInvalidMSISDN
	}

	return MSISDN{value: value}, nil
}

func (m MSISDN) String() string {
	return m.value
}
