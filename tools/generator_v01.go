package main

import (
	"fmt"
	"golang.org/x/exp/maps"
	"math/rand"
	"strings"
	"time"
)

func GenerateFilename(pattern string) string {
	now := time.Now()
	rand.Seed(time.Now().UnixNano())
	siteID := "TUN1"
	cdrTypes := map[string]string{
		"MTSM": "Mobile Terminated Call",
		"MOSM": "Mobile Originated Call",
		"MOSS": "Mobile Originated Short Message",
		"MTSS": "Mobile Terminated Short Message",
	}

	cdrTypesKeys := maps.Keys(cdrTypes)
	cdrType := cdrTypesKeys[rand.Int()%len(cdrTypesKeys)]

	cdrSubTypes := map[string]string{
		"0001": "Voice Call",
		"0002": "SMS",
		"0003": "GPRS",
		"0004": "MMS",
	}

	cdrSubTypesKeys := maps.Keys(cdrSubTypes)
	cdrSubType := cdrSubTypesKeys[rand.Int()%len(cdrSubTypesKeys)]

	replacements := map[string]string{
		"{siteID}":     fmt.Sprintf("%s", siteID),
		"{cdrType}":    fmt.Sprintf("%s", cdrType),
		"{cdrSubType}": fmt.Sprintf("%s", cdrSubType),
		"{YYYY}":       fmt.Sprintf("%d", now.Year()),
		"{MM}":         fmt.Sprintf("%02d", now.Month()),
		"{DD}":         fmt.Sprintf("%02d", now.Day()),
		"{HH}":         fmt.Sprintf("%02d", now.Hour()),
		"{mm}":         fmt.Sprintf("%02d", now.Minute()),
		"{SS}":         fmt.Sprintf("%02d", now.Second()),
		"{cdrSeqNum}":  fmt.Sprintf("%05d", rand.Intn(100000)), // Random 5-digit number
	}

	for placeholder, value := range replacements {
		pattern = strings.ReplaceAll(pattern, placeholder, value)
	}

	return pattern
}

func main() {
	pattern := "{siteID}{MM}{DD}{HH}{MM}{SS}_{cdrType}_{cdrSubType}_CDR{cdrSeqNum}"

	filename := GenerateFilename(pattern)
	fmt.Println("Generated Filename:", filename)
}
