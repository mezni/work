package services

import (
	"math/rand"
	"sync"
	"time"
)

type RandomGenerator struct {
	randSource *rand.Rand
	mu         sync.Mutex
}

func NewRandomGenerator() *RandomGenerator {
	return &RandomGenerator{
		randSource: rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

func (rg *RandomGenerator) GenerateRandomDigits(length int) string {
	rg.mu.Lock()
	defer rg.mu.Unlock()

	digits := make([]byte, length)
	for i := 0; i < length; i++ {
		digits[i] = byte('0' + rg.randSource.Intn(10))
	}
	return string(digits)
}

func (g *RandomGenerator) NextInt64(max int64) int64 {
	g.mu.Lock()
	defer g.mu.Unlock()
	return g.randSource.Int63n(max) // Generates random number in [0, max)
}
