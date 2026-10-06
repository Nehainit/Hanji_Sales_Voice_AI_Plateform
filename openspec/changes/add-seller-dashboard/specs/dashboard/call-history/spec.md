# Spec Delta

## Purpose

Letting the seller see every call, find any order quickly, and check exactly what the
customer said, so they trust the results.

## ADDED Requirements

### Requirement: List of calls, newest first
The calls screen SHALL list every call with time, order number, customer name, city, amount, result and number of tries, newest first.

#### Scenario: Viewing the list
- **WHEN** the seller opens Calls
- **THEN** the 6:42 PM call to Priya Sharma, Jaipur, ₹1,299, Confirmed, 1 try, is above the 6:31 PM call

### Requirement: Filter by result and search
The seller SHALL be able to filter by All, Confirmed, Cancelled, Call later and No answer, each showing its count, and search by customer name, order number or city.

#### Scenario: Cancelled in Jaipur
- **WHEN** the seller picks Cancelled and types "Jaipur"
- **THEN** only cancelled calls for Jaipur customers are listed

#### Scenario: Nothing found
- **WHEN** the search matches no call
- **THEN** the screen says "No calls match. Try a different filter."

### Requirement: Call detail with transcript and recording
Opening a call SHALL show the order, address, tries with times, call length, Shopify tag, cancel reason or new address if any, the full conversation as text, and a button to play the recording.

#### Scenario: Opening a cancelled call
- **WHEN** the seller opens Rahul Verma's cancelled call
- **THEN** they see "Reason: Found it cheaper elsewhere", the full conversation, and can play the recording

#### Scenario: Opening a no-answer order
- **WHEN** the seller opens an order that was never answered
- **THEN** they see the 3 call times and that the customer did not pick up

### Requirement: Customer phone numbers are partly hidden
The calls list SHALL hide the middle digits of customer phone numbers (for example 98290 XXX22). The full number SHALL show only on the call detail.

#### Scenario: Scanning the list
- **WHEN** the seller looks at the list
- **THEN** no full customer phone number is visible

### Requirement: Recordings are kept for 90 days
Recordings and transcripts SHALL be available for 90 days after the call, then deleted. The result and reason SHALL stay.

#### Scenario: Old call
- **WHEN** the seller opens a call from 100 days ago
- **THEN** they see the result and reason, and "Recording deleted after 90 days"
