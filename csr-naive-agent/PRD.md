# Product Requirements Document: Support Application

## 1. Vision
Build a supporting application that manages customer relationships, orders, shipments, and billing records with a clean DDD and Clean Code architecture, enabling scalable development and easy maintenance.

## 2. Problem Statement
The system needs a lightweight yet robust system to manage:
- Customer information and tier segmentation
- Order processing and item tracking
- Shipment tracking with carrier integration
- Billing and transaction history

Existing solutions are either too heavy (enterprise ERP) or too fragmented (separate scripts). Need a unified, modular application.

## 3. Target Users
- Project managers
- Development teams building infrastructure
- Operations teams managing deployments and monitoring

## 4. Success Metrics
- [ ] 100% of CRUD operations covered by unit tests
- [ ] API response time < 200ms for 95% of requests
- [ ] Zero data loss during schema migrations
- [ ] Streamlit UI load time < 3 seconds

## 5. Functional Requirements

### 5.1 Customer Management (Customer Context)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | Create, read, update, delete customers | High |
| FR-02 | Assign tier: Standard, Gold, Enterprise | High |
| FR-03 | Search customers by name/email | Medium |
| FR-04 | View customer billing history | Medium |
| FR-05 | Filter customers by tier | Low |
| FR-21 | Retrieves non-sensitive profile details (name, email, preferences) | Medium |

### 5.2 Order Management (Order Context)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-06 | Create orders with customer association | High |
| FR-07 | Add/remove order items (products, quantities, prices) | High |
| FR-08 | Update order status: Processing → Completed → Returned/Cancelled | High |
| FR-09 | Mark items as eligible/non-eligible for return | Medium |
| FR-25 | Evaluates return windows and policy logic to determine if an item is eligible for refund | Medium |
| FR-26 | Initiates an item return and generates shipping labels; prevents duplicate submissions via idempotency keys | Medium |
| FR-10 | Calculate order total from items | High |
| FR-22 | Fetches past orders, line items, and fulfillment statuses | Medium |

### 5.3 Shipment Management (Shipment Context)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-11 | Create shipments linked to orders | High |
| FR-12 | Assign carrier: FedEx, UPS, DHL | High |
| FR-13 | Track shipments via tracking number | High |
| FR-14 | Update delivery status: In Transit → Out for Delivery → Delivered | High |
| FR-15 | Set estimated delivery dates | Medium |
| FR-23 | Tracks real-time package locations, carriers, and estimated delivery dates | Medium |

### 5.4 Billing Management (Billing Context)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-16 | Create billing records (Charge, Refund, Credit) | High |
| FR-17 | Link billing records to customers | High |
| FR-18 | Track transaction timestamps | Medium |
| FR-19 | Store payment method masks (e.g., "Visa ending in 4242") | Medium |
| FR-20 | View billing history per customer | Low |
| FR-24 | Retrieves payment transactions with masked account/card details (PCI-DSS compliant) | Medium |
| FR-27 | Executes monetary credit to customer balance/payment method; requires explicit auth and full audit logging | High |

## 6. Non-Functional Requirements

### 6.1 Performance
- API response time: < 200ms (p95)
- Database query time: < 50ms for typical lookups
- Streamlit page load: < 3 seconds

### 6.2 Reliability
- SQLite ACID compliance for data integrity
- Graceful degradation if database unavailable
- Automatic reconnection on transient failures

### 6.3 Security
- Email uniqueness constraint
- Payment method masking (never store full card numbers)
- Input validation on all endpoints

### 6.4 Maintainability
- 100% unit test coverage for domain entities
- Documentation generated from code (docstrings)
- Clear separation of concerns (DDD layers)

### 6.5 Scalability
- SQLite for development; PostgreSQL migration path
- Repository pattern enables ORM switching
- No framework coupling in domain layer

## 7. User Stories

### As a...
1. **Project Manager**: "I want to manage customer tiers so I can segment my clients"
2. **Developer**: "I want to create orders with items so I can track project resource allocation"
3. **Operations**: "I want to track shipments so I can monitor deployments"
4. **Finance**: "I want billing records so I can invoice projects"

### Example Flow:
```
User creates Customer → Associates with Orders → Adds Order Items → 
Creates Shipment → Processes Billing Records
```

## 8. Constraints

### 8.1 Technical Constraints
- Must use SQLite for initial development
- Must be compatible with FastAPI and Streamlit
- Domain layer cannot import FastAPI or Streamlit
- Must support Python 3.10+

### 8.2 Business Constraints
- Maximum 5 tier levels for customers
- Order items must have unit price > 0
- Tracking numbers must be unique per shipment
- Billing transactions require amount > 0

### 8.3 Infrastructure Constraints
- Single database file for simplicity (SQLite)
- No external service dependencies initially
- Docker containerizable for deployment

### 8.4 Authentication & Authorization

#### Authentication (authN)
- Users must authenticate via API key or JWT token in `Authorization: Bearer <token>` header
- Token validation performed by FastAPI dependency `get_current_user`
- Session management: tokens valid for 24 hours, refreshable via `/auth/refresh`
- Password policy: minimum 8 characters, mix of upper/lowercase and digits
- Account lockout: 5 failed attempts, 30-minute lockout period

#### Authorization (authZ)
- Permissions scoped by tool catalog authorization levels:
  - `Read` scope: access to `get_customer_account`, `get_order_history`, `get_delivery_status`, `get_billing_history`, `check_refund_eligibility`
  - `Write` scope: access to `create_return_request`
  - `Financial Write` scope: access to `issue_refund` (requires elevated permissions and audit logging)
- Role-based access control (RBAC):
  - **Viewer**: Read-only access to customer/order/summary data
  - **Operator**: Can create orders, add items, create shipments, generate billing records
  - **Manager**: Full CRUD access plus ability to issue refunds and authorize returns
  - **Administrator**: All permissions plus user management and system configuration
- Scope enforcement at FastAPI route level using `Depends(get_current_user_with_scope)`
- All API requests must include valid authentication; unauthenticated requests receive `401 Unauthorized`
- Authorization failures receive `403 Forbidden` with specific error reason

#### AuthN/AuthZ Mapping to Functional Requirements

| FR | Required Scopes | Role Minimum |
|----|-----------------|--------------|
| FR-01 (CRUD customers) | `Read` | Viewer |
| FR-07 (Add order items) | `Write` | Operator |
| FR-08 (Update order status) | `Write` | Operator |
| FR-09 (Mark return eligibility) | `Read` | Viewer/Operator |
| FR-09 (Create return request) | `Write` | Operator |
| FR-16 (Issue refunds) | `Financial Write` | Manager/Administrator |
| FR-13 (Track shipments) | `Read` | Viewer |
| FR-11 (Create shipments) | `Write` | Operator |

## 8. Open Questions / Assumptions

### 8.1 Assumptions
- Single-tenant deployment (one database per organization)
- No concurrent order modification conflicts expected
- Customer tiers are predefined (Standard, Gold, Enterprise)
- Tool catalog authorization will be enforced via FastAPI dependencies

### 8.2 Open Questions
- Should tool endpoints include rate limiting: **NO**
- Email validation strictness level for `get_customer_account`: **NO**
- Shipping cost calculation method integration with `get_delivery_status`: **NO**
- Audit log storage strategy for `issue_refund` operations: **NO**

## 10. Future Considerations

### 10.1 Phase 2 Features
- Webhook notifications for shipment status changes
- Integration with external carrier APIs (FedEx, UPS, DHL)
- Advanced reporting and analytics dashboard
- Multi-tenant support

### 10.2 Phase 3 Features
- Demand forecasting
- Automated billing cycles
- Integration with version control systems
- Notification system (email/SMS)

### 10.3 Technical Debt Paydown
- Migrate from SQLite to PostgreSQL
- Add caching layer (Redis)
- Implement event sourcing for audit trails
- Add GraphQL API alongside REST

---
*Document Version: 1.0*
*Last Updated: 2026-11-08*
*Status: Draft*