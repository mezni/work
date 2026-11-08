# Product Requirements Document: AI Agents Projects Support Application

## 1. Vision
Build a supporting application for AI agents projects that manages customer relationships, orders, shipments, and billing records with a clean DDD and Clean Code architecture, enabling scalable development and easy maintenance.

## 2. Problem Statement
AI agents projects need a lightweight yet robust system to manage:
- Customer information and tier segmentation
- Order processing and item tracking
- Shipment tracking with carrier integration
- Billing and transaction history

Existing solutions are either too heavy (enterprise ERP) or too fragmented (separate scripts). Need a unified, modular application.

## 3. Target Users
- AI agents project managers
- Development teams building AI agent infrastructure
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

### 5.2 Order Management (Order Context)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-06 | Create orders with customer association | High |
| FR-07 | Add/remove order items (products, quantities, prices) | High |
| FR-08 | Update order status: Processing → Completed → Returned/Cancelled | High |
| FR-09 | Mark items as eligible/non-eligible for return | Medium |
| FR-10 | Calculate order total from items | High |

### 5.3 Shipment Management (Shipment Context)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-11 | Create shipments linked to orders | High |
| FR-12 | Assign carrier: FedEx, UPS, DHL | High |
| FR-13 | Track shipments via tracking number | High |
| FR-14 | Update delivery status: In Transit → Out for Delivery → Delivered | High |
| FR-15 | Set estimated delivery dates | Medium |

### 5.4 Billing Management (Billing Context)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-16 | Create billing records (Charge, Refund, Credit) | High |
| FR-17 | Link billing records to customers | High |
| FR-18 | Track transaction timestamps | Medium |
| FR-19 | Store payment method masks (e.g., "Visa ending in 4242") | Medium |
| FR-20 | View billing history per customer | Low |

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
1. **Project Manager**: "I want to manage customer tiers so I can segment my AI agents clients"
2. **Developer**: "I want to create orders with items so I can track AI project resource allocation"
3. **Operations**: "I want to track shipments so I can monitor AI infrastructure deployments"
4. **Finance**: "I want billing records so I can invoice AI agents projects"

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

## 9. Tool Integration

### Tool Catalog Summary

| Tool Name | Authorization Level | Primary Function |
|-----------|--------------------|------------------|
| `get_customer_account` | Read | Retrieves non-sensitive profile details (name, email, preferences). Data filtering applied. |
| `get_order_history` | Read | Fetches past orders, line items, and fulfillment statuses. Customer scope filtering. |
| `get_delivery_status` | Read | Tracks real-time package locations, carriers, and estimated delivery dates. Data filtering. |
| `get_billing_history` | Read (Sensitive-data filtering) | Retrieves payment transactions with masked account/card details (PCI-DSS compliant). |
| `check_refund_eligibility` | Read | Evaluates return windows and policy logic to determine if an item is eligible for refund. Deterministic policy. |
| `create_return_request` | Write (Idempotency) | Initiates an item return and generates shipping labels; prevents duplicate submissions via idempotency keys. |
| `issue_refund` | Financial Write (Elevated permission) | Executes monetary credit to customer balance/payment method; requires explicit auth and full audit logging. |

### Authorization & Policy Mapping

| Functional Requirement | Corresponding Tool(s) | Policy Notes |
|------------------------|----------------------|-------------|
| FR-01: CRUD customers | `get_customer_account` | Read-only access to non-sensitive fields |
| FR-04: View billing history | `get_billing_history` | PCI-DSS masked data only |
| FR-09: Mark return eligibility | `check_refund_eligibility` | Deterministic policy evaluation |
| FR-09: Create return request | `create_return_request` | Idempotency key required; prevents duplicates |
| FR-16: Issue refunds | `issue_refund` | Elevated permission; full audit logging |
| FR-13: Track shipments | `get_delivery_status` | Real-time tracking with carrier data |

### Integration Architecture

The application implements these tools as API endpoints under `/api/v1/tools/` with the following mapping:

- **GET /tools/customer-account** → `get_customer_account`
- **GET /tools/order-history** → `get_order_history`
- **GET /tools/delivery-status** → `get_delivery_status`
- **GET /tools/billing-history** → `get_billing_history`
- **POST /tools/check-refund** → `check_refund_eligibility`
- **POST /tools/create-return** → `create_return_request`
- **POST /tools/issue-refund** → `issue_refund`

Authorization is enforced at the FastAPI route level using dependency injection and scope checks matching the catalog authorization levels.

---

## 8. Open Questions / Assumptions

### 8.1 Assumptions
- Single-tenant deployment (one database per organization)
- No concurrent order modification conflicts expected
- Customer tiers are predefined (Standard, Gold, Enterprise)
- Tool catalog authorization will be enforced via FastAPI dependencies

### 8.2 Open Questions
- Should tool endpoints include rate limiting?
- Email validation strictness level for `get_customer_account`?
- Shipping cost calculation method integration with `get_delivery_status`?
- Audit log storage strategy for `issue_refund` operations?

## 10. Future Considerations

### 10.1 Phase 2 Features
- Webhook notifications for shipment status changes
- Integration with external carrier APIs (FedEx, UPS, DHL)
- Advanced reporting and analytics dashboard
- Multi-tenant support

### 10.2 Phase 3 Features
- AI-powered demand forecasting
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