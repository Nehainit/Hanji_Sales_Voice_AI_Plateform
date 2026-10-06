# Spec Delta

## Purpose

Letting a seller change what the agent says, in their own words, using plain text boxes
instead of flowcharts, and hear the result before customers do.

## ADDED Requirements

### Requirement: Edit each line of the script
The seller SHALL be able to edit these lines: opening, address check, thank-you, ask cancel reason, cancel closing, and ask callback time. The address check and cancel reason SHALL each have an on/off switch.

#### Scenario: Turning off the address check
- **WHEN** the seller switches off "Confirm the address" and saves
- **THEN** on the next call, after "yes" the agent goes straight to the thank-you line

### Requirement: Tap to insert order details
The seller SHALL be able to insert {name}, {brand}, {agent}, {amount}, {product} and {address} by tapping them. These SHALL be replaced with each order's real values on the call.

#### Scenario: Adding the amount
- **WHEN** the seller taps {amount} in the opening line
- **THEN** the preview shows "₹1,299" in that spot for the sample order

### Requirement: Live preview
The editor SHALL show, while typing, how the conversation reads for a sample order (Priya Sharma, Cotton Anarkali Kurti, ₹1,299) for both the yes and the no path.

#### Scenario: Typing a new thank-you line
- **WHEN** the seller types "Shukriya {name} ji!"
- **THEN** the preview immediately shows "Shukriya Priya ji!"

### Requirement: Saved script applies to the next call
A saved script SHALL be used for calls that start after saving. Calls already in progress SHALL keep the old script.

#### Scenario: Save during a busy hour
- **WHEN** the seller saves while 2 calls are in progress
- **THEN** those 2 calls finish with the old script and the next call uses the new one

### Requirement: Mistakes are caught before saving
The editor SHALL NOT save an empty line, a line over 300 characters, or an unknown {placeholder}, and SHALL say what to fix.

#### Scenario: Typo in a placeholder
- **WHEN** the seller types {nam} and taps Save
- **THEN** they see "{nam} is not a known detail. Did you mean {name}?" and nothing is saved

### Requirement: Recording notice cannot be removed
The recording notice SHALL always be spoken at the start of the call, even if the seller removes it from the opening line.

#### Scenario: Seller deletes the notice
- **WHEN** the seller's opening line has no recording notice
- **THEN** the agent still says the recording notice before the opening line

### Requirement: Test and reset
The seller SHALL be able to get a test call with the current script, and reset all lines to the default script.

#### Scenario: Reset
- **WHEN** the seller taps "Reset to default" and confirms
- **THEN** every line goes back to the standard HaanJi script
