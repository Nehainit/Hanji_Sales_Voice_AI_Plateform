# Spec Delta

## Purpose

A prepaid wallet so sellers pay only for calls their customers answer, can top up by UPI in
seconds, and never lose orders when money runs out.

## ADDED Requirements

### Requirement: Free credit on sign-up
Every new seller account SHALL get ₹150 of free credit (50 calls) once.

#### Scenario: New seller
- **WHEN** Kesar Kurtis creates an account
- **THEN** their wallet shows ₹150 and the history shows "Free trial credit +₹150"

### Requirement: Only answered calls are charged
Each answered call SHALL cost ₹3 for up to 1 minute, plus ₹2 for each extra minute or part of a minute. Unanswered, busy, failed and test calls SHALL be free. Prices SHALL be changeable by the admin team for future calls only.

#### Scenario: Short answered call
- **WHEN** a call is answered and lasts 42 seconds
- **THEN** ₹3 is taken from the wallet

#### Scenario: Long answered call
- **WHEN** a call is answered and lasts 1 minute 20 seconds
- **THEN** ₹5 is taken from the wallet

#### Scenario: Not answered
- **WHEN** a call rings with no answer
- **THEN** nothing is taken from the wallet

### Requirement: Wallet screen shows balance and calls left
The wallet screen SHALL show the balance, about how many calls it covers (balance ÷ ₹3), and the price rule in plain words.

#### Scenario: ₹1,840 balance
- **WHEN** the balance is ₹1,840
- **THEN** the screen shows "₹1,840" and "≈ 613 calls left"

### Requirement: Add money by UPI
The seller SHALL be able to pick ₹500, ₹1,000, ₹2,000, ₹5,000 or type an amount (minimum ₹500), pay by UPI, and see the new balance within 1 minute of a successful payment.

#### Scenario: Successful ₹2,000 recharge
- **WHEN** the seller pays ₹2,000 by UPI successfully
- **THEN** within 1 minute the balance goes up by ₹2,000 and the history shows "UPI recharge +₹2,000"

#### Scenario: Payment fails
- **WHEN** the UPI payment fails or is cancelled
- **THEN** the balance does not change and the seller sees "Payment didn't go through. No money was taken."

### Requirement: Low balance alert
When the balance falls below ₹300 (about 100 calls), the seller SHALL see a warning in the app and get an SMS, at most once a day.

#### Scenario: Balance drops to ₹297
- **WHEN** a call charge takes the balance from ₹300 to ₹297
- **THEN** the home screen shows the low balance warning and one SMS is sent that day

### Requirement: Calls pause at zero, orders are not lost
When the balance cannot cover one call, the system SHALL stop placing calls, keep new orders waiting, and tell the seller. After a recharge, waiting orders less than 24 hours old SHALL be called.

#### Scenario: Running out at night
- **WHEN** the balance is ₹2 and 15 orders arrive overnight, and the seller adds ₹1,000 at 10 AM
- **THEN** no calls happen while the balance is ₹2, and all 15 customers are called after 10 AM

### Requirement: Wallet history
The seller SHALL see every wallet change: recharges, free credit, and call charges grouped by day, newest first.

#### Scenario: Checking yesterday
- **WHEN** the seller opens the wallet history
- **THEN** they see "Calls yesterday −₹357" as one line for that day
