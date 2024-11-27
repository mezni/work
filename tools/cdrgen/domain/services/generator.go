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
