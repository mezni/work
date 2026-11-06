# BioViva — Build Order & Dependency Graph

## Build Sequence (from BUILD_PLAN.md:361-378)

```
Phase 0: Project init              (Cargo.toml + crate skeletons + frontend)
Phase 1: cargo build -p bio-core     (no deps)
Phase 2: cargo build -p bio-auth     (bio-core)
Phase 3: cargo build -p bio-products (bio-core)
Phase 3: cargo build -p bio-producers (bio-core)
Phase 3: cargo build -p bio-users    (bio-core + bio-auth)
Phase 3: cargo build -p bio-orders   (all above + bio-auth)
Phase 3: cargo build -p bio-search   (bio-core + bio-products)
Phase 4: cargo build -p bio-api      (ALL 7 crates)
```

## Critical Dependency Paths

| Crate | Direct Dependencies | Hardest Path |
| --- | --- | --- |
| **bio-core** | None (shared kernel) | ✅ Easiest — builds first |
| **bio-auth** | bio-core | ✅ Simple — 1 dep |
| **bio-products** | bio-core | ✅ Simple — 1 dep |
| **bio-producers** | bio-core | ✅ Simple — 1 dep |
| **bio-users** | bio-core, bio-auth | ⚠️ 2 deps but linear |
| **bio-search** | bio-core, bio-products | ✅ 2 deps but independent |
| **bio-orders** | bio-core, bio-products, bio-users, bio-auth, **all others** | ⚠️ **Heaviest** — 5 deps, orders everything else |

## Build Verification Checks

Run these before `cargo build -p bio-api`:

```bash
# 1. Verify workspace resolves
cargo metadata --no-deps --format-version 1 | grep - '"name"' | sort

# 2. Check each crate independently
cargo check -p bio-core
cargo check -p bio-auth
cargo check -p bio-products
cargo check -p bio-producers
cargo check -p bio-users
cargo check -p bio-search

# 3. Finally, the integration test
cargo check -p bio-api   # Fails if any crate has circular/deep deps
```

## Known Build Order Risks

1. **bio-orders depends on ALL other crates** (BUILD_PLAN.md:130-135)
   - If any crate has an undocumented dependency on bio-orders, the build fails
   - **Mitigation**: Repository pattern (AD-3) ensures each crate only accesses its own tables
   - **Sign**: `cargo check -p bio-api` will fail with "unresolved import" if a circular dep exists

2. **bio-search needs bio-users preferences for recommendations**
   - BUILD_PLAN.md:137-142 lists deps as bio-core + bio-products only
   - But feature list includes "Recommendation Engine (trust score + preferences filtering)"
   - **Q-5 in spine** defers this to later (subscription certification renewal logic interacts with freshness)
   - **Watch**: When bio-users implements PreferenceEngine, update bio-search deps

3. **Auth middleware must be mounted before context routers**
   - Per AD-4, `auth_middleware` inserts `Claims` into extensions
   - If any context handler re-implements auth checks, they'll be bypassed
   - **Sign**: All context routers should use `Extension(AuthClaims)` — never re-validate JWT

## Post-Build Verification

After `cargo build -p bio-api` succeeds:

```bash
# Verify the router composition
cd /home/dali/WORK/work/bioviva
# Test public endpoint
curl "http://localhost:3000/api/v1/search?query=olive%20oil"

# Test auth flow
curl -X POST http://localhost:3000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password"}'

# Protected route
TOKEN=$(curl -X POST http://localhost:3000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password"}' | jq -r .access_token)
curl -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/v1/products
```

---

*Derived from BUILD_PLAN.md:361-378, ARCHITECTURE-SPINE.md invariants (AD-2, AD-3, AD-4, AD-7), and .bmad/.memlog.md decisions.*