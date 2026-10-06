# Spec Delta

## Purpose

Putting each call's result where the seller already works: on the Shopify order, or in a
result sheet for uploaded orders, so they know what to ship.

## ADDED Requirements

### Requirement: Shopify order gets a result tag
Within 1 minute of a call result, the Shopify order SHALL get exactly one HaanJi tag: `cod-confirmed`, `cod-cancelled`, `cod-callback` or `cod-no-answer`. A newer result SHALL replace the older HaanJi tag.

#### Scenario: Confirmed order
- **WHEN** Priya confirms order #KK2148 on the call
- **THEN** within 1 minute the order has the tag `cod-confirmed` in Shopify

#### Scenario: Callback later confirmed
- **WHEN** an order tagged `cod-callback` is confirmed on the 7:00 PM call
- **THEN** the tag `cod-callback` is removed and `cod-confirmed` is added

### Requirement: Shopify order gets a short note
The system SHALL add a note to the Shopify order with the result and any detail: the cancel reason, the new address, or the callback time.

#### Scenario: Cancelled with reason
- **WHEN** a customer cancels because "kahin aur sasta mila"
- **THEN** the order note says "HaanJi: Cancelled on call. Reason: Found it cheaper elsewhere."

#### Scenario: New address given
- **WHEN** a customer confirms but gives a new address
- **THEN** the order note shows the new address and says "Please update before shipping"

### Requirement: HaanJi never changes the order itself
The system SHALL NOT cancel, edit or change the address of a Shopify order. It SHALL only add tags and notes.

#### Scenario: Cancelled on the call
- **WHEN** a customer cancels on the call
- **THEN** the Shopify order is still open, with the tag `cod-cancelled`, for the seller to cancel

### Requirement: Result sheet for uploaded orders
For orders from an uploaded sheet, the seller SHALL be able to download a sheet with every original column plus result, cancel reason, new address, callback time and number of tries.

#### Scenario: Download after calling
- **WHEN** all 48 orders from a sheet have a result
- **THEN** the seller downloads a sheet of 48 rows, each with its result filled in
