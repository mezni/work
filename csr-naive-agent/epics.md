---
status: final
stepsCompleted: [1, 2, 3, 4]
inputDocuments: ["PRD.md", "ARCHITECTURE-SPINE.md"]
---

# csr-naive-agent - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for csr-naive-agent, decomposing the requirements from the PRD, Architecture decisions, and into implementable stories.

## Requirements Inventory

### Functional Requirements

FR01: Create, read, update, delete customers  
FR02: Assign tier: Standard, Gold, Enterprise  
FR03: Search customers by name/email  
FR04: View customer billing history  
FR05: Filter customers by tier  
FR21: Retrieves non-sensitive profile details (name, email, preferences)  
FR06: Create orders with customer association  
FR07: Add/remove order items (products, quantities, prices)  
FR08: Update order status: Processing → Completed → Returned/Cancelled  
FR09: Mark items as eligible/non-eligible for return  
FR25: Evaluates return windows and policy logic to determine if an item is eligible for refund  
FR26: Initiates an item return and generates shipping labels; prevents duplicate submissions via idempotency keys  
FR10: Calculate order total from items  
FR22: Fetches past orders, line items, and fulfillment statuses  
FR11: Create shipments linked to orders  
FR12: Assign carrier: FedEx, UPS, DHL  
FR13: Track shipments via tracking number  
FR14: Update delivery status: In Transit → Out for Delivery → Delivered  
FR15: Set estimated delivery dates  
FR23: Tracks real-time package locations, carriers, and estimated delivery dates  
FR16: Create billing records (Charge, Refund, Credit)  
FR17: Link billing records to customers  
FR18: Track transaction timestamps  
FR19: Store payment method masks (e.g., "Visa ending in 4242")  
FR20: View billing history per customer  
FR24: Retrieves payment transactions with masked account/card details (PCI-DSS compliant)  
FR27: Executes monetary credit to customer balance/payment method; requires explicit auth and full audit logging  
FR28: Create, read, update, delete system users  
FR29: Assign roles: Viewer, Operator, Manager, Administrator  
FR30: Manage user permissions scoped by tool catalog  
FR33: User status: active/inactive toggle  
FR34: Search users by name/email

### Non-Functional Requirements

NFR01: API response time: < 200ms (p95)  
NFR02: Database query time: < 50ms for typical lookups  
NFR03: Streamlit page load: < 3 seconds  
NFR04: SQLite ACID compliance for data integrity  
NFR05: Graceful degradation if database unavailable  
NFR06: Automatic reconnection on transient failures  
NFR07: Email uniqueness constraint  
NFR08: Payment method masking (never store full card numbers)  
NFR09: Input validation on all endpoints  
NFR10: Passwords are hashed using bcrypt/Argon2, never stored in plain text  
NFR11: Audit logging for `issue_refund` operations (per FR-27); user management operations (create_user, update_user, delete_user, FR-28/29/30/33) also audited for compliance and access control verification  
NFR12: 100% unit test coverage for domain entities  
NFR13: Documentation generated from code (docstrings)  
NFR14: Clear separation of concerns (DDD layers)  
NFR15: SQLite for development; PostgreSQL migration path  
NFR16: Repository pattern enables ORM switching  
NFR17: No framework coupling in domain layer  
NFR18: Email uniqueness constraint  
NFR19: Payment method masking (never store full card numbers)  
NFR20: Input validation on all endpoints  
NFR21: Passwords are hashed using bcrypt/Argon2, never stored in plain text  
NFR22: Audit logging for `issue_refund` operations; user management operations also audited for compliance  
NFR23: 100% unit test coverage for domain entities  
NFR24: Documentation generated from code (docstrings)  
NFR25: Clear separation of concerns (DDD layers)  
NFR26: SQLite for development; PostgreSQL migration path  
NFR27: Repository pattern enables ORM switching  
NFR28: No framework coupling in domain layer  

### Additional Requirements (from Architecture)

AD-1: Hexagonal architecture with domain layer isolation  
- Binds: FR-01 through FR-34; all NFRs in sections 6.1–6.5; domain entities and use cases  
- Prevents: domain layer importing FastAPI, Streamlit, or tool catalog implementations; direct database coupling in domain models; framework-coupled business rules  
- Rule: The domain layer must not import FastAPI, Streamlit, or any tool catalog SDK. All external interactions go through ports defined in `domain/ports/` and implemented in `application/adapters/`. The repository pattern enables ORM switching.

AD-2: Scope-based authorization with explicit RBAC  
- Binds: AuthN/AuthZ Mapping table (FR-01 to FR-34 → required scopes → role minimum); `Read`/`Write`/`Financial Write`/`User Management` scopes; RBAC roles (Viewer, Operator, Manager, Administrator, User Manager)  
- Prevents: role ambiguity (e.g., Operator performing user management without `User Management` scope); missing scope checks at route level; implicit permission escalation  
- Rule: Every FastAPI route must depend on `get_current_user_with_scope` checking the exact required scope per the AuthN/AuthZ Mapping table. The `User Management` scope is orthogonal to `Read`/`Write`/`Financial Write`; user CRUD operations require explicit `User Management` scope, not general `Write` scope.

AD-3: Repository pattern for ORM independence  
- Binds: Scalability section (SQLite → PostgreSQL migration path); repository pattern enablement in domain layer  
- Prevents: domain entities referencing SQLAlchemy models directly; hard-coded SQL queries in use cases; migration breakage when switching databases  
- Rule: Domain entities use plain Python types (no SQLAlchemy imports). Repository interfaces live in `domain/ports/`; concrete repositories using SQLAlchemy live in `infrastructure/repositories/`. The application layer depends on domain repositories, not on SQLAlchemy models.

AD-4: PCI-DSS compliant payment data handling  
- Binds: FR-24 (payment transactions with masked account/card details); NFR 6.3 Security (payment method masking)  
- Prevents: storage of full card numbers in any database or log; unmasked card data in API responses or error messages  
- Rule: Card numbers must never be stored. Payment method data stored as masked format (e.g., "Visa ending in 4242") or tokenized. The `get_billing_history` tool returns only masked data. Any card data received from clients must be masked immediately at the API boundary.

AD-5: Audit logging scope  
- Binds: FR-27 (issue_refund operations); user management operations (create_user, update_user, delete_user, FR-28/29/30/33); NFR 6.3 Security audit logging clause  
- Prevents: unaudited monetary transactions; unlogged user lifecycle events; audit log gaps for compliance  
- Rule: Every `issue_refund` request must produce an audit log entry with: timestamp, user ID, refund amount, order ID, reason. User management CRUD operations (FR-28/29/30/33) must also produce audit entries. Audit logs stored in compliant storage (initial: SQLite; future: dedicated audit store). Log entries include user identity, operation type, timestamp, and outcome (success/failure).

AD-6: Password hashing requirement  
- Binds: NFR 6.3 Security (passwords hashed using bcrypt/Argon2); authN section password policy  
- Prevents: plain-text password storage in database; password reuse without hashing; compliance failures  
- Rule: All user passwords must be hashed using bcrypt or Argon2 at the point of creation/update. Never stored in plain text. Password policy: minimum 8 characters, mix of upper/lowercase and digits, account lockout after 5 failed attempts (30-minute lockout). The authN layer handles verification; the domain layer never sees raw passwords.

### FR Coverage Map

| Epic | Covering FRs |
|------|-------------|
| Epic 1: Customer Management | FR-01, FR-02, FR-03, FR-04, FR-05, FR-21 |
| Epic 2: Order Management | FR-06, FR-07, FR-08, FR-09, FR-10, FR-22, FR-25, FR-26 |
| Epic 3: Shipment Management | FR-11, FR-12, FR-13, FR-14, FR-15, FR-23 |
| Epic 4: Billing Management | FR-16, FR-17, FR-18, FR-19, FR-20, FR-24, FR-27 |
| Epic 5: User Management | FR-28, FR-29, FR-30, FR-33, FR-34 |

## Epic List

### Epic 1: Customer Management

**Epic Goal:** Enable creation, modification, and querying of customer profiles with tier segmentation and preference tracking.

**Stories:** (5 stories planned)

### Epic 2: Order Management

**Epic Goal:** Enable order creation, item management, return processing, and order history retrieval.

**Stories:** (8 stories planned)

### Epic 3: Shipment Management

**Epic Goal:** Enable shipment creation, carrier assignment, real-time tracking, and delivery status updates.

**Stories:** (6 stories planned)

### Epic 4: Billing Management

**Epic Goal:** Enable billing record creation, payment transaction history, refund processing, and PCI-DSS compliant payment data handling.

**Stories:** (7 stories planned)

### Epic 5: User Management

**Epic Goal:** Enable system user administration, role-based access control, and permission management with full audit logging.

**Stories:** (5 stories planned)

## Epics and Stories Detail

Epic 1: Customer Management
----------------------------------------
Story 1.1: As a customer service representative, I want to create a new customer profile with name, email, and tier assignment, so that I can onboard new clients to the system.

**Acceptance Criteria:**
- Given I am authenticated with sufficient permissions
- When I provide customer name, email, and tier
- Then the system creates a customer with unique email constraint
- And assigns the specified tier (Standard, Gold, Enterprise)
- And returns the created customer ID and details

Story 1.2: As a customer service representative, I want to update an existing customer's tier and preferences, so that I can reflect changes in the customer relationship.

**Acceptance Criteria:**
- Given I am authenticated with sufficient permissions
- When I provide customer ID and new tier/preferences
- Then the system updates the customer's tier and preferences
- And returns the updated customer record
- And logs the update in the audit trail

Story 1.3: As a customer service representative, I want to search for customers by name or email, so that I can quickly locate customer profiles.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide a name or email search term
- Then the system returns matching customers
- And results are filtered by the search term
- And no results are returned if no match exists

Story 1.4: As a customer service representative, I want to view a customer's billing history, so that I can understand their payment patterns.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide customer ID
- Then the system returns the customer's billing records
- And records are shown with masked payment details
- And the list includes transaction types and amounts

Story 1.5: As a project manager, I want to filter customers by tier, so that I can segment my client base for targeting.

**Acceptance Criteria:**
- Given I am authenticated with sufficient permissions
- When I filter by tier (Standard, Gold, Enterprise)
- Then the system returns customers matching the tier
- And the count is displayed

Epic 2: Order Management
----------------------------------------
Story 2.1: As a customer, I want to create an order with selected items, quantities, and prices, so that I can purchase products through the system.

**Acceptance Criteria:**
- Given I am authenticated
- When I provide product IDs, quantities, and prices
- Then the system creates an order associated with my customer account
- And calculates the order total from item prices
- And returns the order ID and status (initially Processing)

Story 2.2: As a customer service representative, I want to add or remove order items (products, quantities, prices), so that I can modify orders before they are fulfilled.

**Acceptance Criteria:**
- Given I am authenticated with Write scope
- When I provide order ID and item modifications
- Then the system adds or removes items from the order
- And recalculates the order total
- And returns the updated order record

Story 2.3: As a customer service representative, I want to update order status through its lifecycle (Processing → Completed → Returned/Cancelled), so that I can reflect the order's fulfillment state.

**Acceptance Criteria:**
- Given I am authenticated with Write scope
- When I provide order ID and target status
- Then the system updates the order status following the valid transition path
- And prevents invalid status transitions
- And returns the updated order record

Story 2.3.1: [Conditional] As a customer service representative, I want to mark items as eligible or non-eligible for return, so that I can determine return eligibility.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide item ID and eligibility status
- Then the system marks the item as eligible or non-eligible for return
- And returns the updated item status
- And the determination follows the policy logic

Story 2.4: As a customer, I want to evaluate whether an item is eligible for a refund based on return windows and policy logic, so that I know if I can return a purchase.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide item ID and purchase date
- Then the system evaluates return windows and policy logic
- And determines if the item is eligible for refund
- And returns a deterministic eligibility decision

Story 2.5: As a customer service representative, I want to initiate an item return and generate shipping labels, so that I can process returns without duplicate submissions.

**Acceptance Criteria:**
- Given I am authenticated with Write scope
- When I provide item ID and reason for return
- And include an idempotency key
- Then the system initiates the return request
- And generates shipping labels
- And prevents duplicate submissions via idempotency key validation
- And returns the return request ID and label status

Story 2.6: As a customer service representative, I want to fetch past orders with their line items and fulfillment statuses, so that I can review order history.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide customer ID
- Then the system returns past orders
- And each order includes line items (products, quantities, prices)
- And fulfillment statuses are shown for each order

Epic 3: Shipment Management
----------------------------------------
Story 3.1: As a customer service representative, I want to create a shipment linked to an order, so that I can initiate tracking and delivery.

**Acceptance Criteria:**
- Given I am authenticated with Write scope
- When I provide order ID and carrier (FedEx, UPS, DHL)
- Then the system creates a shipment linked to the order
- And assigns a tracking number
- And returns the shipment ID and initial status

Story 3.2: As a customer, I want to track shipments via tracking number, so that I can see real-time package locations and delivery status.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide a tracking number
- Then the system returns real-time package location
- And carrier information
- And estimated delivery date
- And current delivery status (In Transit, Out for Delivery, Delivered)

Story 3.3: As a customer service representative, I want to update delivery status through its lifecycle (In Transit → Out for Delivery → Delivered), so that I can reflect the shipment's progress.

**Acceptance Criteria:**
- Given I am authenticated with Write scope
- When I provide shipment ID and status update
- Then the system updates the delivery status following valid transitions
- And prevents invalid status transitions
- And returns the updated shipment record

Story 3.4: As a customer service representative, I want to set estimated delivery dates for shipments, so that I can communicate expected delivery times.

**Acceptance Criteria:**
- Given I am authenticated with Write scope
- When I provide shipment ID and estimated delivery date
- Then the system stores the estimated delivery date
- And returns the updated shipment record
- The date follows the format: ISO 8601

Story 3.5: As a customer, I want to track real-time package locations, carriers, and estimated delivery dates, so that I know where my order is and when to expect it.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide shipment ID or tracking number
- Then the system returns current package location
- And carrier name
- And estimated delivery date
- And status indicators

Epic 4: Billing Management
----------------------------------------
Story 4.1: As a customer service representative, I want to create billing records (Charge, Refund, Credit), so that I can process financial transactions.

**Acceptance Criteria:**
- Given I am authenticated with Financial Write scope
- When I provide order ID, customer ID, and transaction type (Charge/Refund/Credit)
- And provide amount and payment details
- Then the system creates a billing record
- And links it to the customer and order
- And returns the billing record ID and status

Story 4.2: As a customer service representative, I want to link billing records to customers, so that I can track transaction history per customer.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide customer ID
- Then the system returns all billing records associated with the customer
- And records include transaction timestamps
- And payment method details are masked (PCI-DSS compliant)

Story 4.3: As a customer service representative, I want to track transaction timestamps, so that I can understand the timing of financial events.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide billing record ID
- Then the system returns the transaction timestamp
- And the timestamp follows ISO 8601 format
- And the timezone is documented

Story 4.4: As a customer, I want to view payment transactions with masked account/card details (PCI-DSS compliant), so that I can see my billing history without exposing sensitive data.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide customer ID
- Then the system returns payment transactions
- And card numbers are never displayed in full
- And payment methods show masked format (e.g., "Visa ending in 4242")
- And the system never stores full card numbers

Story 4.5: As a customer service representative, I want to execute monetary credit to customer balance or payment method, so that I can process refunds or credits.

**Acceptance Criteria:**
- Given I am authenticated with Financial Write scope
- When I provide customer ID, amount, and credit destination
- And have explicit auth and full audit logging
- Then the system executes the monetary credit
- And records the transaction in the audit log
- And returns the credit confirmation and updated balance

Story 4.6: As a customer service representative, I want to evaluate return windows and policy logic to determine if an item is eligible for refund, so that I can process refund requests correctly.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide item ID and purchase date
- Then the system evaluates return windows and policy logic
- And determines if the item is eligible for refund
- And returns a deterministic eligibility decision
- The policy is deterministic and consistent across identical inputs

Epic 5: User Management
----------------------------------------
Story 5.1: As a system administrator, I want to create, read, update, and delete system users, so that I can manage system access.

**Acceptance Criteria:**
- Given I am authenticated with User Management scope
- When I provide user details (name, email, role assignment)
- Then the system creates a user with the specified role
- And returns the created user ID and role
- And the `User Management` scope is explicitly required (not general `Write` scope)

Story 5.2: As a system administrator, I want to assign roles (Viewer, Operator, Manager, Administrator) to users, so that I can control system access levels.

**Acceptance Criteria:**
- Given I am authenticated with User Management scope
- When I provide user ID and target role
- Then the system assigns the specified role to the user
- And the role determines available scopes and operations
- And returns the updated user record with role

Story 5.3: As a system administrator, I want to manage user permissions scoped by tool catalog, so that I can control which tools each user can access.

**Acceptance Criteria:**
- Given I am authenticated with User Management scope
- When I provide user ID and tool catalog permissions
- Then the system assigns the specified tool catalog permissions
- And the `User Management` scope is required
- And returns the updated user record with permissions

Story 5.4: As a system administrator, I want to toggle user status (active/inactive), so that I can deactivate or reactivate user accounts.

**Acceptance Criteria:**
- Given I am authenticated with Administrator role (not just Write scope)
- When I provide user ID and target status (active/inactive)
- Then the system toggles the user's active status
- And returns the updated user record
- And the operation is audited for compliance

Story 5.5: As a customer service representative, I want to search for users by name or email, so that I can locate user accounts.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide a name or email search term
- Then the system returns matching users
- And results are filtered by the search term
- And no results are returned if no match exists

## Requirements Coverage Map

| Epic | Covering FRs | Key NFRs | Key ADs |
|------|-------------|----------|---------|
| Epic 1: Customer Management | FR-01 to FR-05, FR-21 | NFR07, NFR18, NFR01 | AD-2 |
| Epic 2: Order Management | FR-06 to FR-10, FR-22, FR-25, FR-26 | NFR01, NFR09, NFR11, NFR15 | AD-1, AD-2, AD-5 |
| Epic 3: Shipment Management | FR-11 to FR-15, FR-23 | NFR01, NFR03, NFR15 | AD-1 |
| Epic 4: Billing Management | FR-16 to FR-20, FR-24, FR-27 | NFR08, NFR10, NFR11, NFR15 | AD-4, AD-5, AD-6 |
| Epic 5: User Management | FR-28 to FR-30, FR-33, FR-34 | NFR11, NFR17, NFR01, NFR07 | AD-2, AD-3, AD-5, AD-6 |

## Generated Stories

Total stories: 289
### Story 1.1: Customer Registration with Email


**As a** customer service representative,


**I want** create a new customer profile with name, email, and tier assignment,


**So that** onboard new clients to the system.


**Acceptance Criteria:**


**Given** I am authenticated with sufficient permissions


**When** I provide customer name, email, and tier


**Then** the system creates a customer with unique email constraint

and assigns the specified tier (Standard, Gold, Enterprise)

and returns the created customer ID and details


### Story 1.2: Customer Tier and Preferences Update


**As a** customer service representative,


**I want** update an existing customer's tier and preferences,


**So that** reflect changes in the customer relationship.


**Acceptance Criteria:**


**Given** I am authenticated with sufficient permissions


**When** I provide customer ID and new tier/preferences


**Then** the system updates the customer's tier and preferences

and returns the updated customer record

and logs the update in the audit trail


### Story 1.3: Customer Search by Name/Email


**As a** customer service representative,


**I want** search for customers by name or email,


**So that** quickly locate customer profiles.


**Acceptance Criteria:**


**Given** I am authenticated with Read scope


**When** I provide a name or email search term


**Then** the system returns matching customers

and results are filtered by the search term

and no results are returned if no match exists


### Story 1.4: View Customer Billing History


**As a** customer service representative,


**I want** view a customer's billing history,


**So that** understand their payment patterns.


**Acceptance Criteria:**


**Given** I am authenticated with Read scope


**When** I provide customer ID


**Then** the system returns the customer's billing records

and records are shown with masked payment details

and the list includes transaction types and amounts


### Story 1.5: Filter Customers by Tier


**As a** project manager,


**I want** filter customers by tier,


**So that** segment client base for targeting.


**Acceptance Criteria:**


**Given** I am authenticated with sufficient permissions


**When** I filter by tier (Standard, Gold, Enterprise)


**Then** the system returns customers matching the tier

and the count is displayed

and the filter applies to all tier levels


### Story 2.1: Order Creation with Items


**As a** customer,


**I want** create an order with selected items, quantities, and prices,


**So that** purchase products through the system.


**Acceptance Criteria:**


**Given** I am authenticated


**When** I provide product IDs, quantities, and prices


**Then** the system creates an order associated with my customer account

and calculates the order total from item prices

and returns the order ID and status (initially Processing)


### Story 2.2: Add/Remove Order Items


**As a** customer service representative,


**I want** add or remove order items (products, quantities, prices),


**So that** modify orders before they are fulfilled.


**Acceptance Criteria:**


**Given** I am authenticated with Write scope


**When** I provide order ID and item modifications


**Then** the system adds or removes items from the order

and recalculates the order total

and returns the updated order record


### Story 2.3: Update Order Status Lifecycle


**As a** customer service representative,


**I want** update order status through its lifecycle (Processing -> Completed -> Returned/Cancelled),


**So that** reflect the order's fulfillment state.


**Acceptance Criteria:**


**Given** I am authenticated with Write scope


**When** I provide order ID and target status


**Then** the system updates the order status following the valid transition path

and prevents invalid status transitions

and returns the updated order record


### Story 2.4: Return Eligibility


**As a** customer service representative,


**I want** mark items as eligible or non-eligible for return,


**So that** determine return eligibility.


**Acceptance Criteria:**


**Given** I am authenticated with Read scope


**When** I provide item ID and eligibility status


**Then** the system marks the item as eligible or non-eligible for return

and returns the updated item status

and the determination follows the policy logic


### Story 2.5: Evaluate Refund Eligibility


**As a** customer,


**I want** evaluate whether an item is eligible for a refund based on return windows and policy logic,


**So that** know if I can return a purchase.


**Acceptance Criteria:**


**Given** I am authenticated with Read scope


**When** I provide item ID and purchase date


**Then** the system evaluates return windows and policy logic

and determines if the item is eligible for refund

and returns a deterministic eligibility decision

the policy is deterministic and consistent across identical inputs


### Story 2.6: Initiate Return Request


**As a** customer service representative,


**I want** initiate an item return and generate shipping labels; prevents duplicate submissions via idempotency keys,


**So that** process returns without duplicate submissions.


**Acceptance Criteria:**


**Given** I am authenticated with Write scope


**When** I provide item ID and reason for return


and include an idempotency key


**Then** the system initiates the return request

and generates shipping labels

and prevents duplicate submissions via idempotency key validation

and returns the return request ID and label status


### Story 2.7: Fetch Past Orders with Line Items


**As a** customer service representative,


**I want** fetch past orders with their line items and fulfillment statuses,


**So that** review order history.


**Acceptance Criteria:**


**Given** I am authenticated with Read scope


**When** I provide customer ID


**Then** the system returns past orders

and each order includes line items (products, quantities, prices)

and fulfillment statuses are shown for each order


### Story 3.1: Create Shipment Linked to Order


**As a** customer service representative,


**I want** create a shipment linked to an order,


**So that** initiate tracking and delivery.


**Acceptance Criteria:**


**Given** I am authenticated with Write scope


**When** I provide order ID and carrier (FedEx, UPS, DHL)


**Then** the system creates a shipment linked to the order

and assigns a tracking number

and returns the shipment ID and initial status


### Story 3.2: Track Shipments via Tracking Number


**As a** customer,


**I want** track shipments via tracking number,


**So that** see real-time package locations and delivery status.


**Acceptance Criteria:**


**Given** I am authenticated with Read scope


**When** I provide a tracking number


**Then** the system returns real-time package location

and carrier information

and estimated delivery date

and current delivery status (In Transit, Out for Delivery, Delivered)


### Story 3.3: Update Delivery Status Lifecycle


**As a** customer service representative,


**I want** update delivery status through its lifecycle (In Transit -> Out for Delivery -> Delivered),


**So that** reflect the shipment's progress.


**Acceptance Criteria:**


**Given** I am authenticated with Write scope


**When** I provide shipment ID and status update


**Then** the system updates the delivery status following valid transitions

and prevents invalid status transitions

and returns the updated shipment record


### Story 3.4: Set Estimated Delivery Dates


**As a** customer service representative,


**I want** set estimated delivery dates for shipments,


**So that** communicate expected delivery times.


**Acceptance Criteria:**


**Given** I am authenticated with Write scope


**When** I provide shipment ID and estimated delivery date


**Then** the system stores the estimated delivery date

and returns the updated shipment record

the date follows the format: ISO 8601


### Story 3.5: Real-Time Package Tracking


**As a** customer,


**I want** track real-time package locations, carriers, and estimated delivery dates,


**So that** know where my order is and when to expect it.


**Acceptance Criteria:**


**Given** I am authenticated with Read scope


**When** I provide shipment ID or tracking number


**Then** the system returns current package location

and carrier name

and estimated delivery date

and status indicators


### Story 4.1: Create Billing Records


**As a** customer service representative,


**I want** create billing records (Charge, Refund, Credit),


**So that** process financial transactions.


**Acceptance Criteria:**


**Given** I am authenticated with Financial Write scope


**When** I provide order ID, customer ID, and transaction type (Charge/Refund/Credit)


and provide amount and payment details


**Then** the system creates a billing record

and links it to the customer and order

and returns the billing record ID and status


### Story 4.2: Link Billing Records to Customers


**As a** customer service representative,


**I want** link billing records to customers,


**So that** track transaction history per customer.


**Acceptance Criteria:**


**Given** I am authenticated with Read scope


**When** I provide customer ID


**Then** the system returns all billing records associated with the customer

and records include transaction timestamps

and payment method details are masked (PCI-DSS compliant)


### Story 4.3: Track Transaction Timestamps


**As a** customer service representative,


**I want** track transaction timestamps,


**So that** understand the timing of financial events.


**Acceptance Criteria:**


**Given** I am authenticated with Read scope


**When** I provide billing record ID


**Then** the system returns the transaction timestamp

and the timestamp follows ISO 8601 format

and the timezone is documented


### Story 4.4: View PCI-DSS Compliant Payment Transactions


**As a** customer,


**I want** view payment transactions with masked account/card details (PCI-DSS compliant),


**So that** see billing history without exposing sensitive data.


**Acceptance Criteria:**


**Given** I am authenticated with Read scope


**When** I provide customer ID


**Then** the system returns payment transactions

and card numbers are never displayed in full

and payment methods show masked format (e.g., 'Visa ending in 4242')

and the system never stores full card numbers


### Story 4.5: Execute Monetary Credit


**As a** customer service representative,


**I want** execute monetary credit to customer balance or payment method,


**So that** process refunds or credits.


**Acceptance Criteria:**


**Given** I am authenticated with Financial Write scope


**When** I provide customer ID, amount, and credit destination


and have explicit auth and full audit logging


**Then** the system executes the monetary credit

and records the transaction in the audit log

and returns the credit confirmation and updated balance


### Story 4.6: Evaluate Return Policy for Refund


**As a** customer service representative,


**I want** evaluate return windows and policy logic to determine if an item is eligible for refund,


**So that** process refund requests correctly.


**Acceptance Criteria:**


**Given** I am authenticated with Read scope


**When** I provide item ID and purchase date


**Then** the system evaluates return windows and policy logic

and determines if the item is eligible for refund

and returns a deterministic eligibility decision

the policy is deterministic and consistent across identical inputs


### Story 5.1: Create System Users


**As a** system administrator,


**I want** create, read, update, delete system users,


**So that** manage system access.


**Acceptance Criteria:**


**Given** I am authenticated with User Management scope


**When** I provide user details (name, email, role assignment)


**Then** the system creates a user with the specified role

and returns the created user ID and role

and the User Management scope is explicitly required (not general Write scope)


### Story 5.2: Assign User Roles


**As a** system administrator,


**I want** assign roles (Viewer, Operator, Manager, Administrator) to users,


**So that** control system access levels.


**Acceptance Criteria:**


**Given** I am authenticated with User Management scope


**When** I provide user ID and target role


**Then** the system assigns the specified role to the user

and the role determines available scopes and operations

and returns the updated user record with role


### Story 5.3: Manage User Permissions by Tool Catalog


**As a** system administrator,


**I want** manage user permissions scoped by tool catalog,


**So that** control which tools each user can access.


**Acceptance Criteria:**


**Given** I am authenticated with User Management scope


**When** I provide user ID and tool catalog permissions


**Then** the system assigns the specified tool catalog permissions

and the User Management scope is required

and returns the updated user record with permissions


### Story 5.4: Toggle User Status Active/Inactive


**As a** system administrator,


**I want** toggle user status (active/inactive),


**So that** deactivate or reactivate user accounts.


**Acceptance Criteria:**


**Given** I am authenticated with Administrator role (not just Write scope)


**When** I provide user ID and target status (active/inactive)


**Then** the system toggles the user's active status

and returns the updated user record

and the operation is audited for compliance


### Story 5.5: Search Users by Name/Email


**As a** customer service representative,


**I want** search for users by name or email,


**So that** locate user accounts.


**Acceptance Criteria:**


**Given** I am authenticated with Read scope


**When** I provide a name or email search term


**Then** the system returns matching users

and results are filtered by the search term

and no results are returned if no match exists


---

**Story generation complete.** All 28 stories across 5 epics have been generated and appended.
Each story follows the template format from step-03-create-stories.md.
All FRs are mapped to epics via the FR Coverage Map in the document.
