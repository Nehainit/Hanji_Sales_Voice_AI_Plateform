# Spec Delta

## Purpose

Letting the seller control when and how calls go out, which orders come in, and the numbers
used to show money saved.

## ADDED Requirements

### Requirement: Calling time settings
The seller SHALL be able to set the wait after an order (2, 5, 15 or 60 minutes), calling hours (start and end, between 7 AM and 10 PM), retries (1, 2 or 3 tries) and the gap between tries (30 minutes, 1, 2 or 4 hours). The start time SHALL be before the end time.

#### Scenario: Later start
- **WHEN** the seller sets calling hours to 10 AM–8 PM and saves
- **THEN** an order at 9:30 AM gets its first call at 10:00 AM

#### Scenario: Wrong hours
- **WHEN** the seller sets start 9 PM and end 9 AM
- **THEN** they see "Start time must be before end time" and nothing is saved

### Requirement: Voice and language settings
The seller SHALL be able to change the voice and call language at any time. Changes SHALL apply from the next call.

#### Scenario: Switching to Meera
- **WHEN** the seller changes the voice to Meera and saves
- **THEN** the next call uses Meera's voice

### Requirement: Order sources
The settings SHALL show whether Shopify is connected, let the seller disconnect it, and let them upload an order sheet.

#### Scenario: Disconnecting Shopify
- **WHEN** the seller taps Disconnect and confirms
- **THEN** no new Shopify orders come in and planned calls for that store are cancelled

### Requirement: RTO cost per order
The seller SHALL be able to set their RTO cost per order (default ₹160), which is used for "money saved".

#### Scenario: Higher shipping cost
- **WHEN** the seller sets the RTO cost to ₹200
- **THEN** money saved this month is recalculated with ₹200

### Requirement: Pause and resume calling
The seller SHALL be able to pause all calls and resume them. While paused, new orders SHALL be saved but not called; on resume, orders still unconfirmed and less than 24 hours old SHALL be called.

#### Scenario: Pausing during a holiday
- **WHEN** the seller pauses calling and 20 orders arrive, then resumes 3 hours later
- **THEN** all 20 customers get called after resuming, inside calling hours
