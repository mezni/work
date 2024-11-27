package services

import (
	"math/rand"
	"sync"
)

func generateRandomDigits(length int, randSource *rand.Rand, mu *sync.Mutex) string {
	mu.Lock()
	defer mu.Unlock()

	digits := make([]byte, length)
	for i := 0; i < length; i++ {
		digits[i] = byte('0' + randSource.Intn(10))
	}
	return string(digits)
}
