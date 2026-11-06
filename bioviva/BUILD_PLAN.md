# BioViva - Build Plan

Based on the architecture documented in ARCHITECTURE_SUMMARY.md, here's the complete build plan for the BioViva ecommerce system.

## Prerequisites

```bash
# Install tools
rustup toolchain install 1.70
cargo install sqlx-cli      # for DB migrations
docker install              # for containerization
npm create vite@latest      # for frontend
```

---

## Phase 0: Project Setup

### 0.1 Create Root Cargo.toml
```bash
cd /home/dali/WORK/work/bioviva
cat > Cargo.toml << 'EOF'
[workspace]

members = [
    "services/bio-auth",
    "services/bio-core", 
    "services/bio-products",
    "services/bio-producers",
    "services/bio-orders",
    "services/bio-users",
    "services/bio-search",
    "services/bio-api",
    "src",
    "frontend",
]
EOF
```

### 0.2 Initialize Each Crate

```bash
# Initialize all service crates
cd /home/dali/WORK/work/bioviva/services
for crate in bio-auth bio-core bio-products bio-producers bio-users bio-search bio-api; do
  echo "Initializing $crate..."
  cargo init --name "$crate" 2>&1 | grep -v "help:" | grep -v "note:"
done

# Create src/main.rs for each (minimal)
for crate in bio-auth bio-products bio-producers bio-users bio-search bio-api; do
  touch /home/dali/WORK/work/bioviva/services/$crate/src/main.rs
done
```

### 0.3 Setup Frontend

```bash
cd /home/dali/WORK/work/bioviva
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
# Add Axum API client
npm install axios @tanstack/react-query
```

---

## Phase 1: Core Domain (bio-core)

```bash
# Build bio-core first (no external deps)
cargo build -p bio-core

# Verify
cargo check -p bio-core
```

**Implement** in `services/bio-core/src/main.rs`:
- `TrustScore` value object (0-100)
- `FreshnessState` enum (Fresh/Ripe/Aging/Archived)
- `ProductId`, `Sku`, `Money` primitives
- `BioError` error type with context
- Shared enum types (product types, certification status, user roles)

---

## Phase 2: Authentication Service (bio-auth)

```bash
cargo build -p bio-auth
```

**Implement** in `services/bio-auth/src/main.rs`:
- `Claims` struct for JWT (sub, role, scopes, iat, exp)
- `AuthService` with login/register/refresh/logout
- `Argon2Hasher` for password hashing/verification
- `permission_required()` and `role_required()` middleware functions
- JWT configuration loading from env env vars

**Database migrations** (run separately, see Phase 6):
- Extend `users` table: `password_hash`, `role`, `failed_login_attempts`, `account_locked_until`
- Create `oauth2_tokens` table (optional)

---

## Phase 3: Bounded Contexts (build in dependency order)

### 3.1 `bio-products` (depends on bio-core)
```bash
cargo build -p bio-products
```

**Implement** product aggregates, `TasteProfile`, `AromaNote`, `ProductRepository` trait, `FreshnessCalculator`, `TrustScoreCalculator`, handlers: `list_products`, `get_product`, `search_products`.

### 3.2 `bio-producers` (depends on bio-core)
```bash
cargo build -p bio-producers
```

**Implement**: Producer aggregates, Certification, HarvestBatch, Repository traits, CertificationValidator.

### 3.3 `bio-users` (depends on bio-core + bio-auth)
```bash
cargo build -p bio-users
```

**Implement**: User/Profile/TasteQuizResult/Preference entities, Repository traits, TasteQuizEngine, PreferenceEngine.

### 3.4 `bio-orders` (depends on bio-core + bio-products + bio-users + bio-auth)
```bash
cargo build -p bio-orders
```

**Implement**: Order/Subscription aggregates, OrderRepository/SubscriptionRepository traits, OrderValidator (freshness windows), SubscriptionManager (certification renewal), FreshnessEligibilityChecker.

### 3.5 `bio-search` (depends on bio-core + bio-products)
```bash
cargo build -p bio-search
```

**Implement**: SearchQuery/SearchResult/Recommendation entities, RecommendationEngine (trust score + preferences filtering), TrustFilter, seasonal availability filtering.

### 3.6 `bio-api` (depends on ALL 7 crates above)
```bash
cargo build -p bio-api
```

**Implement** `src/main.rs`:
- `sqlx::pool::Pool` - single connection pool from `DATABASE_URL`
- Axum router composition with nested routes:
  - `/api/v1/auth` → bio-auth
  - `/api/v1/products` → bio-products
  - `/api/v1/producers` → bio-producers
  - `/api/v1/orders` → bio-orders
  - `/api/v1/users` → bio-users
  - `/api/v1/search` → bio-search
- CORS middleware config
- Tracing subscriber setup
- Fallback handler for React SPA (`index.html`)
- `Extension(AuthClaims)` injection pattern

**.env.example** (create at project root):
```
DATABASE_URL=postgres://bio:bio@localhost/bioviva
JWT_SECRET=base64-encoded-32-bytes-min
JWT_EXPIRES_MIN=30
REFRESH_TOKEN_EXPIRES_DAYS=30
ARGON2_MEMORY=64
ARGON2_TIME=3
ARGON2_PARALLEL=2
ACCOUNT_LOCKOUT_AFTER=5
ACCOUNT_LOCKOUT_MINUTES=30
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## Phase 4: Frontend Integration

```bash
cd /home/dali/WORK/work/bioviva/frontend
npm run dev  # development server
```

**API client** (`src/api/client.ts`):
```typescript
import axios from 'axios';
import { useQuery } from '@tanstack/react-query';

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

// Attach JWT from localStorage
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const useProducts = (query = '') => 
  useQuery(['products', query], () => api.get(`/search?query=${query}`));
```

**Integration with Axum**: In Docker, copy built frontend dist to `./static`. In dev, Vite proxies `/api` to `http://localhost:3000`.

---

## Phase 5: Database Migrations

```bash
# Initialize sqlx
sqlx init  # creates sqlx.json

# Create initial migration
sqlx migrate add create_tables

# Edit up.sql with key tables (see ARCHITECTURE_SUMMARY.md p76-95):
-- users table (extended for auth)
-- products table (with trust_score, freshness_state, harvest_date, batch_number)
-- producers, certifications, orders, order_lines, subscriptions
-- oauth2_tokens, password_resets

# Run migrations
sqlx migrate run
# Or: cargo run --bin bio-api (with migrations embedded)
```

---

## Phase 6: Docker Build

### 6.1 Multi-Stage Dockerfile (in `/home/dali/WORK/work/bioviva/Dockerfile`)

```dockerfile
# Stage 1: Build
FROM rust:1.70 AS builder
WORKDIR /app
COPY Cargo.toml .
RUN cargo fetch
COPY src ./src
COPY frontend ./frontend
RUN cargo build --release  # builds bio-api + all deps

# Stage 2: Run
FROM ubuntu:22.04 AS runtime
WORKDIR /app
COPY --from=builder /app/target/release/bio-app .
COPY --from=builder /app/frontend/dist ./static  # frontend
EXPOSE 3000
CMD ["./bio-app"]  # Axum serves API + static from /
```

### 6.2 Build and Run

```bash
docker build -t bioivva:latest .
docker run -d -p 3000:3000 \
  -e DATABASE_URL="postgres://bio:bio@localhost/bioviva" \
  -e JWT_SECRET="base64-encoded-32-bytes" \
  -e CORS_ORIGINS="http://localhost:3000" \
  bioivva:latest
```

### 6.3 Verify Running API

```bash
# Test public endpoint
curl "http://localhost:3000/api/v1/search?query=olive%20oil"

# Test auth flow
curl -X POST http://localhost:3000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password"}'

# Protected route (with token from login above)
TOKEN=$(curl -X POST http://localhost:3000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password"}' | jq -r .access_token)
curl -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/v1/products
```

---

## Phase 7: Testing

```bash
# Unit tests (all crates)
cargo test --workspace

# Specific crate tests
cargo test -p bio-auth
cargo test -p bio-api

# Integration test example (in bio-api tests/)
#[tokio::test]
async fn test_login_and_protected_route() {
    let pool = sqlx::postgres::PgPool::connect("postgres://localhost/bioviva_test").await.unwrap();
    # Register user, login, get JWT, call protected endpoint, assert 200 OK
}
```

---

## Phase 8: Deployment

### 8.1 Production Docker

```bash
docker build -t bioivva/production:latest .
docker push bioivva/production:latest
```

### 8.2 Environment Variables for Production

```env
# .env.production
DATABASE_URL=postgres://user:password@prod-db-host/bioviva_prod
JWT_SECRET=prod-jwt-secret-min-32-bytes-base64
REFRESH_TOKEN_EXPIRES_DAYS=90
ARGON2_MEMORY=128
ARGON2_TIME=5
ARGON2_PARALLEL=4
ACCOUNT_LOCKOUT_AFTER=5
ACCOUNT_LOCKOUT_MINUTES=15
CORS_ORIGINS=https://domain.com,https://api.domain.com
```

### 8.3 Docker Compose (optional)

```yaml
version: "3.9"
services:
  api:
    image: bioivva/production:latest
    ports: ["3000:3000"]
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - JWT_SECRET=${JWT_SECRET}
      - CORS_ORIGINS=${CORS_ORIGINS}
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=bioviva_prod
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

---

## Build Sequence Summary

```
Phase 0: Project init          (Cargo.toml + crate skeletons + frontend)
Phase 1: cargo build -p bio-core     (no deps)
Phase 2: cargo build -p bio-auth     (bio-core)
Phase 3: cargo build -p bio-products (bio-core)
Phase 3: cargo build -p bio-producers (bio-core)
Phase 3: cargo build -p bio-users    (bio-core + bio-auth)
Phase 3: cargo build -p bio-orders   (all above + bio-auth)
Phase 3: cargo build -p bio-search   (bio-core + bio-products)
Phase 4: cargo build -p bio-api      (ALL 7 crates)
Phase 5: npm create vite + npm install (frontend)
Phase 6: sqlx migrate add + run      (DB schema)
Phase 7: docker build + docker run   (container)
Phase 8: cargo test --workspace    (verify)
Phase 9: docker push / docker-compose up (deploy)
```

**Critical Build Order**: Build from top to bottom. Each `cargo build` must succeed before moving down. `bio-api` is last since it depends on all 7 service crates.

**Expected Build Time**: ~5-10 minutes total (incremental builds are faster once crates are compiled).