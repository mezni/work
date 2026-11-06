#!/usr/bin/env bash
set -euo pipefail

# BioViva Build Verification Script
# Runs before cargo build to ensure all prerequisites are met

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKDIR="$PROJECT_ROOT"

echo "========================================="
echo "BioViva Build Verification"
echo "========================================="
echo

# 1. Rust toolchain check
echo "=== Checking Rust toolchain ==="
if ! command -v rustc &>/dev/null; then
    echo "FAIL: rustc not found in PATH"
    exit 1
fi

RUST_VERSION=$(rustc --version | awk '{print $2}')
MAJOR_MINOR=$(echo "$RUST_VERSION" | cut -d. -f1,2)
echo "Rust version: $RUST_VERSION (required: 1.70)"

if [ "$MAJOR_MINOR" != "1.70" ]; then
    echo "WARN: Rust 1.70 recommended, but $RUST_VERSION detected"
else
    echo "OK: Rust 1.70 confirmed"
fi
echo

# 2. Cargo workspace check
echo "=== Checking Cargo workspace ==="
if [ -f "$PROJECT_ROOT/Cargo.toml" ]; then
    echo "OK: Root Cargo.toml exists"
    # Check workspace members
    MEMBERS_COUNT=$(grep -c '^members' "$PROJECT_ROOT/Cargo.toml" || echo "0")
else
    echo "GREENFIELD: Root Cargo.toml not yet created (will be Phase 0)"
    MEMBERS_COUNT=0
fi
echo

# 3. Crate skeletons check (may be greenfield)
echo "=== Checking crate skeletons ==="
EXPECTED_CRATES="bio-auth bio-core bio-products bio-producers bio-orders bio-users bio-search bio-api"
MISSING=0

for crate in $EXPECTED_CRATES; do
    if [ -d "services/$crate" ]; then
        echo "OK: services/$crate/ exists"
        if [ -f "services/$crate/Cargo.toml" ]; then
            echo "  → Cargo.toml found"
        else
            echo "  ⚠ Cargo.toml missing"
            MISSING=$((MISSING + 1))
        fi
        if [ -f "services/$crate/src/main.rs" ]; then
            echo "  → main.rs found"
        else
            echo "  ⚠ main.rs missing"
            MISSING=$((MISSING + 1))
        fi
    else
        echo "GREENFIELD: services/$crate/ not yet created (Phase 0 will create it)"
        # Don't count as missing - Phase 0 creates these
    fi
done
echo

# 4. Frontend setup check
echo "=== Checking frontend setup ==="
if [ -d "frontend" ]; then
    echo "OK: frontend/ directory exists"
    if [ -f "frontend/package.json" ]; then
        echo "OK: frontend/package.json exists"
    else
        echo "WARN: frontend/package.json missing"
        MISSING=$((MISSING + 1))
    fi
    if [ -f "frontend/src/api/client.ts" ]; then
        echo "OK: frontend/src/api/client.ts exists"
    else
        echo "WARN: frontend/src/api/client.ts missing"
        MISSING=$((MISSING + 1))
    fi
else
    echo "MISSING: frontend/ directory"
    MISSING=$((MISSING + 1))
fi
echo

# 5. Dockerfile check
echo "=== Checking Docker configuration ==="
if [ -f "Dockerfile" ]; then
    echo "OK: Dockerfile exists"
    if grep -q "rust:1.70" Dockerfile; then
        echo "OK: Dockerfile uses rust:1.70 builder image"
    else
        echo "WARN: Dockerfile builder image may not be rust:1.70"
        MISSING=$((MISSING + 1))
    fi
    if grep -q "COPY.*frontend" Dockerfile; then
        echo "OK: Dockerfile copies frontend dist"
    else
        echo "WARN: Dockerfile may not copy frontend dist"
        MISSING=$((MISSING + 1))
    fi
else
    echo "MISSING: Dockerfile"
    MISSING=$((MISSING + 1))
fi
echo

# 6. .env.example check
echo "=== Checking environment configuration ==="
if [ -f ".env.example" ]; then
    echo "OK: .env.example exists"
    # Check for key vars
    for var in DATABASE_URL JWT_SECRET ACCOUNT_LOCKOUT_AFTER; do
        if grep -q "^${var}=" .env.example; then
            echo "  OK: $var defined"
        else
            echo "  WARN: $var not found in .env.example"
            MISSING=$((MISSING + 1))
        fi
    done
else
    echo "MISSING: .env.example"
    MISSING=$((MISSING + 1))
fi
echo

# 7. Memlog and spine check
echo "=== Checking architecture spine artifacts ==="
if [ -f ".bmad/.memlog.md" ]; then
    echo "OK: .bmad/.memlog.md exists"
else
    echo "WARN: .bmad/.memlog.md missing (architecture spine not initialized)"
    MISSING=$((MISSING + 1))
fi

if [ -f "ARCHITECTURE-SPINE.md" ]; then
    echo "OK: ARCHITECTURE-SPINE.md exists"
else
    echo "WARN: ARCHITECTURE-SPINE.md missing (architecture spine not initialized)"
    MISSING=$((MISSING + 1))
fi
echo

# Summary
echo "========================================="
echo "Verification Summary"
echo "========================================="
if [ "$MISSING" -eq 0 ]; then
    echo "All checks passed. Ready to build."
    exit 0
else
    echo "$MISSING issue(s) found. Fix before building."
    exit 1
fi