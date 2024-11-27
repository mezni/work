package services

import (
	"errors"
	"math/rand"
	"net"
)

type IPVersion int

const (
	IPv4 IPVersion = iota
	IPv6
)

type IPType int

const (
	Public IPType = iota
	Private
)

var (
	ErrInvalidIPVersion = errors.New("invalid IP version: must be IPv4 or IPv6")
	ErrInvalidIPType    = errors.New("invalid IP type: must be Public or Private")
)

type IPGenerator struct {
	randomGenerator *RandomGenerator
}

func NewIPGenerator() *IPGenerator {
	return &IPGenerator{randomGenerator: NewRandomGenerator()}
}

func (g *IPGenerator) GenerateIP(version IPVersion, ipType IPType) (string, error) {
	switch version {
	case IPv4:
		return g.generateIPv4(ipType)
	case IPv6:
		return g.generateIPv6(ipType)
	default:
		return "", ErrInvalidIPVersion
	}
}

func (g *IPGenerator) generateIPv4(ipType IPType) (string, error) {
	privateRanges := [][]int{
		{10, 0, 0, 0, 8},     // 10.0.0.0/8
		{172, 16, 0, 0, 12},  // 172.16.0.0/12
		{192, 168, 0, 0, 16}, // 192.168.0.0/16
	}

	if ipType == Private {
		rangeIndex := g.randomGenerator.randSource.Intn(len(privateRanges))
		base := privateRanges[rangeIndex]
		return g.randomIPv4(base[:4], base[4]), nil
	}

	return g.randomIPv4(nil, 0), nil
}

func (g *IPGenerator) generateIPv6(ipType IPType) (string, error) {
	if ipType == Private {
		// Private IPv6 range: fc00::/7
		return g.randomIPv6(net.ParseIP("fc00::")), nil
	}

	// Public IPv6 range
	return g.randomIPv6(nil), nil
}

func (g *IPGenerator) randomIPv4(base []int, prefix int) string {
	ip := make([]int, 4)
	for i := range ip {
		ip[i] = rand.Intn(256)
	}
	if base != nil {
		for i := 0; i < len(base); i++ {
			ip[i] = base[i]
		}
	}
	return net.IPv4(byte(ip[0]), byte(ip[1]), byte(ip[2]), byte(ip[3])).String()
}

func (g *IPGenerator) randomIPv6(base net.IP) string {
	ip := make([]byte, 16)
	if base != nil {
		copy(ip, base)
	}
	for i := 0; i < len(ip); i++ {
		ip[i] ^= byte(rand.Intn(256))
	}
	return net.IP(ip).String()
}
