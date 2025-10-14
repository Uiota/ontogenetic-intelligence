module github.com/Uiota/ontogenetic-intelligence

go 1.21

require (
	// Core (Air-gap only)
	github.com/spf13/cobra v1.7.0

	// Cryptography (Zero-trust)
	golang.org/x/crypto v0.12.0

	// Database (Mini OS)
	gorm.io/gorm v1.25.4
	gorm.io/driver/sqlite v1.5.3

	// Utilities
	gopkg.in/yaml.v3 v3.0.1
)

// Air-gap compliance
replace (
	golang.org/x/crypto => ./vendor/x-crypto
)