# Spec Delta

## Purpose

Bringing a seller's cash-on-delivery orders into HaanJi, from their Shopify store or from an
uploaded sheet, so each one can get a confirmation call.

## ADDED Requirements

### Requirement: New Shopify COD orders arrive automatically
When a connected Shopify store gets a new order paid by cash on delivery, the system SHALL save it within 1 minute with the customer name, phone, amount, products and address.

#### Scenario: COD order placed
- **WHEN** Priya Sharma places a ₹1,299 COD order on kesarkurtis.myshopify.com
- **THEN** within 1 minute the order is saved in HaanJi and queued for a call

### Requirement: Prepaid orders are ignored
The system SHALL NOT call customers for orders that are already paid online.

#### Scenario: UPI-paid order
- **WHEN** a customer pays ₹899 by UPI at checkout
- **THEN** the order is not saved for calling and no call is made

### Requirement: Same order is never added twice
If Shopify sends the same order more than once, the system SHALL keep only one copy and plan only one set of calls.

#### Scenario: Shopify resends an order
- **WHEN** Shopify sends order #KK2148 twice
- **THEN** there is one order #KK2148 and one planned call

### Requirement: Orders without a usable phone are flagged
Orders with a missing or invalid phone number SHALL be saved as **Can't call: phone missing** and shown to the seller, with no call made.

#### Scenario: Phone missing
- **WHEN** an order arrives with an empty phone field
- **THEN** no call is planned and the order is marked Can't call: phone missing

### Requirement: Seller can upload a sheet of orders
A seller SHALL be able to upload a CSV or Excel file with the columns order_id, customer_name, phone, amount, product and address. The system SHALL show how many rows are ready and list each problem row by row number before any call starts.

#### Scenario: Sheet with two bad rows
- **WHEN** a seller uploads a sheet of 50 rows where row 5 has no phone and row 9 has no amount
- **THEN** the system shows "48 orders ready" and "Row 5: phone missing, Row 9: amount missing"

### Requirement: Sheet calls start only when the seller says so
Calls for uploaded orders SHALL start only after the seller presses "Start calling".

#### Scenario: Seller reviews first
- **WHEN** a sheet is uploaded but the seller has not pressed Start calling
- **THEN** no customer from that sheet is called

### Requirement: Store disconnect stops new orders
When a seller removes the HaanJi app from Shopify, the system SHALL stop taking new orders and cancel all planned calls for that store.

#### Scenario: App uninstalled
- **WHEN** Kesar Kurtis uninstalls the app with 12 calls still planned
- **THEN** none of those 12 calls are made
