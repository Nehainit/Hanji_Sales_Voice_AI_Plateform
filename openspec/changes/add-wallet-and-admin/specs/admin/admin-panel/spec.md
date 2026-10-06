# Spec Delta

## Purpose

One place for the HaanJi team to see every seller, what calls cost us versus what we earn,
and to fix account problems safely, without touching the database by hand.

## ADDED Requirements

### Requirement: Only the team can open the admin panel
Only accounts marked as HaanJi team members SHALL be able to open the admin panel. Everyone else SHALL see "You don't have access to this page."

#### Scenario: Seller tries the admin link
- **WHEN** a seller opens the admin panel address
- **THEN** they see the no-access message and no seller data

### Requirement: List of all sellers
The admin panel SHALL list every seller with brand name, status (Setting up, Live, Paused, Out of balance), wallet balance, calls today and sign-up date, with search by brand name or phone.

#### Scenario: Finding a seller
- **WHEN** a team member searches "Kesar"
- **THEN** Kesar Kurtis is listed with status Live, balance ₹1,840 and 128 calls today

### Requirement: Cost and margin
The admin panel SHALL show, per day and per seller, what calls cost us (phone, speech and AI), what sellers paid, and the margin (paid minus cost).

#### Scenario: Daily margin
- **WHEN** yesterday had 1,000 answered calls charged ₹3,200 in total and costing ₹1,350
- **THEN** the panel shows earned ₹3,200, cost ₹1,350, margin ₹1,850

### Requirement: Add free credit with a reason
A team member SHALL be able to add credit to a seller's wallet only with a written reason. Each credit SHALL be recorded with who added it and when.

#### Scenario: Goodwill credit
- **WHEN** a team member adds ₹300 to Kesar Kurtis with the reason "Calls failed on 6 Oct"
- **THEN** the seller's balance goes up by ₹300 and the record shows the team member, the time and the reason

#### Scenario: No reason given
- **WHEN** a team member tries to add credit with an empty reason
- **THEN** nothing is added and they see "Please write a reason"

### Requirement: Pause and resume a seller
A team member SHALL be able to pause and resume any seller's calling, with a reason. While paused by the team, the seller SHALL see "Calling paused by HaanJi support" and cannot resume it themselves.

#### Scenario: Pausing for complaints
- **WHEN** a team member pauses a seller with the reason "Customer complaints, checking script"
- **THEN** that seller's calls stop and the seller sees the support message

### Requirement: Failed calls view
The admin panel SHALL list calls that failed for technical reasons in the last 7 days, with seller, time and error, so the team can spot problems.

#### Scenario: Phone network outage
- **WHEN** 40 calls failed between 2:00 and 2:20 PM with the same network error
- **THEN** they appear together in the failed calls list with that error
