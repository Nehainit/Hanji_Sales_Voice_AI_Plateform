# Spec Delta

## Purpose

Placing phone calls from our business number to customers, and reporting what happened to
each call so the rest of the system can act on it.

## ADDED Requirements

### Requirement: Calls Indian mobile numbers only
The system SHALL call only valid Indian mobile numbers (10 digits starting with 6, 7, 8 or 9, optionally with +91, 91 or 0 in front). Other numbers SHALL NOT be called and SHALL be marked **Invalid number**.

#### Scenario: Valid number with +91
- **WHEN** the order phone is "+91 98290 41122"
- **THEN** the system calls 9829041122

#### Scenario: Number too short
- **WHEN** the order phone is "98290 411"
- **THEN** no call is placed and the result is Invalid number

### Requirement: Same business number every time
Every call SHALL show the same HaanJi business number to the customer.

#### Scenario: Two different orders
- **WHEN** two customers get calls for two different brands
- **THEN** both see the same HaanJi business number

### Requirement: Reports what happened to the call
For every call, the system SHALL record one status: **Answered**, **Busy**, **Not answered** or **Failed**, within 1 minute of the call ending.

#### Scenario: Customer does not pick up
- **WHEN** the phone rings for 30 seconds with no answer
- **THEN** the call status Not answered is saved within 1 minute

#### Scenario: Network problem
- **WHEN** the call cannot connect because of a phone network error
- **THEN** the status Failed is saved with the error, and the customer is not charged as an answered call

### Requirement: One call at a time per customer
The system SHALL NOT start a new call to a phone number that is already on a call with us.

#### Scenario: Duplicate trigger
- **WHEN** a second call is requested for 9829041122 while the first is still going
- **THEN** the second call is not placed

### Requirement: Test call with a sample order
A team member SHALL be able to start a test call to any phone number using a sample order, and get the same record as a real call.

#### Scenario: Founder tests on own phone
- **WHEN** a team member starts a test call to their own number with the sample order "Priya Sharma, Cotton Anarkali Kurti, ₹1,299"
- **THEN** their phone rings, the full COD conversation runs, and the call record is saved and marked as a test
