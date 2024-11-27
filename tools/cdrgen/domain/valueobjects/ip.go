package valueobjects

import (
	"errors"
	"net"
)

var ErrInvalidIPAddress = errors.New("invalid IP address format")

type IP struct {
	value string
}

func NewIP(value string) (IP, error) {
	if net.ParseIP(value) == nil {
		return IP{}, ErrInvalidIPAddress
	}
	return IP{value: value}, nil
}

func (i IP) String() string {
	return i.value
}
