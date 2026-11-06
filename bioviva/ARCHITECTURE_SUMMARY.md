# BioViva - DDD + Clean Code + Rust + Axum Architecture

## Overall Principle
Single Axum application with one shared PostgreSQL database. Each bounded context is a separate crate/module with clear domain boundaries, sharing the same DB connection. Single Docker container serves the Axum app (which serves static frontend + API).

## Crate/Service Structure

### 0. `bio-auth` - Authentication & Authorization Context
- **JWT issuance & validation**: access tokens (15-30 min) + refresh tokens (7-30 days)
- **Role-Based Access Control (RBAC)**: roles `guest|buyer|producer|admin` with scoped permissions
- **Password handling**: Argon2 hashing, validation (min 12 chars, mixed types)
- **Token revocation**: blacklist on logout
- **Middleware**: Axum `auth_middleware` (extracts/validates JWT, inserts `Claims` into extensions), `permission_middleware` / `role_middleware`
- **Database**: extends `users` table with `password_hash`, `role`, `failed_login_attempts`, `account_locked_until`; `oauth2_tokens` for social login
- **Key invariants**: JWT signature verified per request, role-permission checks before handler execution, password never stored in plaintext, account lockout after N failed attempts
- **Clean code**: Zero business logic beyond auth concerns; depends on `bio-core` and `bio-users` repo trait; all other crates depend on auth only via request extensions

### 1. `bio-core` - Shared Kernel
- **Domain primitives**: `Money`, `ProductId`, `Sku`, `BatchNumber`
- **Error types**: `BioError`, `NotFound`, `ValidationFailed`
- **Value objects**: `TrustScore`, `FreshnessState`, `OriginCoordinates`
- **DB shared types**: connection pool config, migration traits, enums shared across contexts
- **Clean code**: Zero runtime dependencies beyond shared DB driver

### 2. `bio-products` - Product Bounded Context
- **Domain**: Olive oil, honey, herbal essences aggregates
- **Entities**: `Product`, `ProductVariant`, `TasteProfile`, `AromaNote`
- **Repositories**: `ProductRepository`, `VariantRepository`
- **Services**: `ProductAvailabilityService`, `FreshnessCalculator`
- **Axum handlers**: `GET /products`, `GET /products/{id}`, `GET /products/search`
- **Key invariants**: Trust score calculation, freshness lifecycle (Fresh/Ripe/Aging/Archived), harvest date validation

### 3. `bio-producers` - Producer Bounded Context
- **Domain**: Farmer/beekeeper/herb grower aggregates
- **Entities**: `Producer`, `Certification`, `HarvestBatch`, `LabResult`
- **Repositories**: `ProducerRepository`, `CertificationRepository`, `HarvestRepository`
- **Services**: `CertificationValidator`, `TrustScoreCalculator`, `QualityAssessor`
- **Axum handlers**: `GET /producers`, `GET /producers/{id}`, `POST /producers`
- **Key invariants**: Certification validity checks, producer reputation scoring, batch traceability

### 4. `bio-orders` - Order/Commerce Bounded Context
- **Domain**: Purchase orders, subscriptions, reordering
- **Entities**: `Order`, `OrderLine`, `Subscription`, `ReorderCycle`
- **Repositories**: `OrderRepository`, `SubscriptionRepository`, `PaymentRepository`
- **Services**: `OrderValidator`, `SubscriptionManager`, `FreshnessEligibilityChecker`
- **Axum handlers**: `POST /orders`, `GET /orders/{id}`, `POST /orders/{id}/subscribe`, `GET /reorders`
- **Key invariants**: Order only valid for Fresh/Ripe products, subscription manages certification renewal, reorder respects freshness windows

### 5. `bio-users` - User/Account Bounded Context
- **Domain**: User profiles, preferences, taste quizzes
- **Entities**: `User`, `Profile`, `TasteQuizResult`, `Preference`
- **Repositories**: `UserRepository`, `PreferenceRepository`
- **Services**: `TasteQuizEngine`, `PreferenceEngine`, `SubscriptionManager`
- **Axum handlers**: `GET /profile`, `PUT /profile`, `POST /quiz`, `GET /recommendations`
- **Key invariants**: User controls data visibility, preferences influence recommendation trust score, quiz data informs product filtering

### 6. `bio-search` - Discovery Bounded Context
- **Domain**: Product search, filtering, recommendation
- **Entities**: `SearchQuery`, `SearchResult`, `Recommendation`
- **Services**: `ElasticSearchIntegration`, `RecommendationEngine`, `TrustFilter`
- **Axum handlers**: `GET /search`, `GET /recommendations`, `GET /trending`
- **Key invariants**: Results filtered by minimum trust score, seasonal availability, user preference matching

### 7. `bio-api` - Axum Application Entry Point
- **Main**: `main.rs` - starts Axum server, configures DB pool, registers routers
- **Router**: Combines all bounded context routers with versioned prefixes
  - `api/v1/products` → `bio-products`
  - `api/v1/producers` → `bio-producers`
  - `api/v1/orders` → `bio-orders`
  - `api/v1/users` → `bio-users`
  - `api/v1/search` → `bio-search`
- **Static file serving**: Axum serves React/Vite build from `/frontend/dist`
- **CORS**, **middleware** (logging, tracing, error handling)
- **Single Docker**: `FROM rust:latest` build, `COPY --from=builder`, runs `axum-app`

## Database Schema (Shared - One PostgreSQL)

### Core Tables (shared across contexts)
- `products` - all product data (olive oil, honey, essences)
- `producers` - farmer/ producer data
- `certifications` - organic, fair trade, etc.
- `orders` - purchase orders
- `users` - account data (extended with password_hash, role, etc.)
- `search_index` - full-text search vector
- `oauth2_tokens` - social login tokens (optional)

### Context-Specific Tables
- `product_taste_profiles` - `bio-products` crate
- `product_aroma_notes` - `bio-products` crate
- `harvest_batches` - `bio-producers` crate
- `order_lines` - `bio-orders` crate
- `subscriptions` - `bio-orders` crate
- `user_preferences` - `bio-users` crate
- `taste_quiz_results` - `bio-users` crate
- `password_resets` - `bio-auth` crate (temporary tokens)

## Data Access Pattern

### Repository Pattern (per context)
Each crate implements its own Repository trait that abstracts DB access:

```rust
// bio-products trait
trait ProductRepository: Send + Sync + 'static {
    async fn find_by_id(&self, id: ProductId) -> Result<Product, BioError>;
    async fn find_trust_above(&self, min_score: TrustScore) -> Vec<Product>;
    async fn find_freshest(&self, limit: usize) -> Vec<Product>;
    async fn update_trust_score(&self, id: ProductId, score: TrustScore) -> Result<(), BioError>;
}
```

### Shared DB Connection
- Single ` deadpool-postgres ` or `sqlx ` connection pool in `bio-core`
- All crates receive pool via dependency injection
- Each crate only accesses its own tables (enforced by code review, not DB schema isolation)

## Axum Router Structure

### Auth Routes (mounted at `/api/v1/auth`)
```rust
router::Router::new()
    .route("/login", post(auth::login_handler))
    .route("/refresh", post(auth::refresh_handler))
    .route("/logout", post(auth::logout_handler))
    .route("/register", post(auth::register_handler))
```

### Bounded Context Routes
```rust
router::Router::new()
    .route("/products", get(list_products).post(create_product))
    .route("/products/:id", get(get_product).put(update_product))
    .route("/producers", get(list_producers).post(create_producer))
    .route("/orders", post(create_order).get(list_orders))
    .route("/search", get(search_products))
    .route("/profile", get(get_profile).put(update_profile))
```

### Full Main Router Composition
```rust
#[axum::main]
async fn main() {
    // ... init tracing, db pool ...
    
    let app = router::Router::new()
        .route("/api/v1/auth/login", post(login_handler))
        .route("/api/v1/auth/refresh", post(refresh_handler))
        .route("/api/v1/auth/logout", post(logout_handler))
        .route("/api/v1/auth/register", post(register_handler))
        .nest("/api/v1", {
            router::Router::new()
                .route("/products", get(list_products).post(create_product))
                .route("/products/:id", get(get_product).put(update_product))
                .route("/producers", get(list_producers).post(create_producer))
                .route("/orders", post(create_order).get(list_orders))
                .route("/search", get(search_products))
                .route("/profile", get(get_profile).put(update_profile))
        })
        .fallback(fallback_handler);  // serves SPA
}
```

## Docker Configuration

### Single Multi-Stage Dockerfile

```dockerfile
# Stage 1: Build
FROM rust:1.70 AS builder
WORKDIR /app
COPY Cargo.toml .
RUN cargo fetch
COPY src ./src
RUN cargo build --release

# Stage 2: Run
FROM ubuntu:22.04 AS runtime
WORKDIR /app
COPY --from=builder /app/target/release/bio-app .
COPY frontend/dist ./static  # Frontend build
EXPOSE 3000
CMD ["./bio-app"]  # Axum serves API + static from /
```

### What the container runs
- Axum HTTP server on port 3000
- `/api/v1/auth/*` → auth routes (login, refresh, logout, register)
- `/api/v1/*` → bounded context routes (products, producers, orders, search, profile)
- `/` → serves `index.html` (React SPA fallback)
- All API calls go to same localhost:3000
- Database connection via environment variable `DATABASE_URL`
- JWT secret from `JWT_SECRET` env var (minimum 256 bits, base64-encoded)
- Access token expiry: `JWT_EXPIRES_MIN` (default 30 minutes)
- Refresh token expiry: `REFRESH_TOKEN_EXPIRES_DAYS` (default 30 days)
- Argon2 params: `ARGON2_MEMORY` (default 64MB), `ARGON2_TIME` (default 3), `ARGON2_PARALLEL` (default 2)
- Account lockout: `ACCOUNT_LOCKOUT_AFTER` failed attempts (default 5), `ACCOUNT_LOCKOUT_MINUTES` (default 30)
- CORS origins from `CORS_ORIGINS` (comma-separated list)

## Clean Code Principles Applied

1. **Single Responsibility**: Each crate has one reason to change
2. **Open/Closed**: Add new bounded contexts without modifying existing ones
3. **Liskov Substitution**: Repository traits interchangeable
4. **Interface Segregation**: Small, focused traits per context
5. **Dependency Injection**: DB pool inverted - crates depend on abstractions
6. **Explicit Dependencies**: `Cargo.toml` shows exact crates used per module
7. **Error Handling**: `BioError` with context-preserving context objects, no panics