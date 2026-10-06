# Spec Delta

## Purpose

Deciding when each customer gets called, so calls happen soon after the order, only at
polite hours, with sensible retries and no calls once the order is settled.

## ADDED Requirements

### Requirement: First call after a short wait
The first call SHALL happen after the seller's chosen wait time (2, 5, 15 or 60 minutes; default 5) from when the order was placed.

#### Scenario: Default wait
- **WHEN** an order is placed at 10:00 AM with the default settings
- **THEN** the first call happens at 10:05 AM

### Requirement: Calls only inside calling hours
Calls SHALL only happen inside the seller's calling hours (default 9:00 AM to 9:00 PM IST). A call that falls outside SHALL move to the start of the next calling window.

#### Scenario: Late-night order
- **WHEN** an order is placed at 8:58 PM with a 5-minute wait
- **THEN** the first call happens at 9:00 AM the next morning

#### Scenario: Early-morning order
- **WHEN** an order is placed at 2:00 AM
- **THEN** the first call happens at 9:00 AM the same day

### Requirement: Unanswered calls are retried
If a call is not answered, busy or failed, the system SHALL try again after the seller's gap (default 2 hours), up to the seller's limit (default 3 tries in total). After the last try the order SHALL be marked **No answer**.

#### Scenario: Second try
- **WHEN** a 12:00 PM call is not answered and it was the first try
- **THEN** the next try is at 2:00 PM

#### Scenario: Out of tries
- **WHEN** the third try is not answered
- **THEN** no more calls are made and the order is marked No answer

#### Scenario: Retry falls after hours
- **WHEN** a try at 8:00 PM is not answered
- **THEN** the next try is at 9:00 AM the next morning

### Requirement: Callback at the time the customer asked
When a call ends as **Call later** with a time, the next call SHALL happen at that time (moved into calling hours if needed). If that call is not answered, normal retries apply.

#### Scenario: Customer asked for 7 PM
- **WHEN** a customer says "shaam 7 baje call karna" at 1:15 PM
- **THEN** the next call is at 7:00 PM the same day

#### Scenario: Customer asked for 11 PM
- **WHEN** a customer asks to be called at 11:00 PM
- **THEN** the next call is at 9:00 AM the next morning

#### Scenario: Call later without a time
- **WHEN** a call ends as Call later because the answer was unclear, at 3:00 PM
- **THEN** the next call follows the normal retry gap, at 5:00 PM

### Requirement: No calls once the order is settled
The system SHALL cancel all planned calls for an order once it is Confirmed or Cancelled, or when the seller cancels the order in Shopify.

#### Scenario: Seller cancels in Shopify first
- **WHEN** the seller cancels order #KK2148 in Shopify before its 10:05 AM call
- **THEN** the 10:05 AM call is not made
