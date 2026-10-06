# Spec Delta

## Purpose

The seller's home screen: shows in plain words and rupees what the calls achieved, and what
needs the seller's action, so they see the value at a glance.

## ADDED Requirements

### Requirement: Money saved this month
The home screen SHALL show the RTO money saved this month as: orders cancelled on a call before shipping × the seller's RTO cost per order, with that calculation written below the number.

#### Scenario: 293 cancellations at ₹160
- **WHEN** 293 orders were cancelled on calls this month and the RTO cost is ₹160
- **THEN** the screen shows "₹46,880" and "293 orders cancelled before shipping × ₹160"

### Requirement: Today's numbers
The home screen SHALL show today's calls, Confirmed (with % of calls), Cancelled (with money saved), and No answer / Call later.

#### Scenario: A normal day
- **WHEN** today had 128 calls: 97 confirmed, 14 cancelled, 17 no answer or later
- **THEN** the screen shows 128, 97 (76%), 14 (₹2,240 saved at ₹160) and 17

### Requirement: Last 7 days chart with a table option
The home screen SHALL show a chart of the last 7 days split into Confirmed, Cancelled and No answer / later, with a legend, the exact numbers on tap or hover, and a button to see the same numbers as a table.

#### Scenario: Seller taps Saturday
- **WHEN** the seller taps Saturday's bar
- **THEN** they see Saturday's confirmed, cancelled and no-answer counts

### Requirement: Needs your attention list
The home screen SHALL list things the seller must act on: customers who gave a new address, upcoming callbacks, orders that can't be called, and a low wallet balance. Tapping an item SHALL open the related screen.

#### Scenario: Address changes waiting
- **WHEN** 3 customers gave new addresses today
- **THEN** the list shows "3 customers asked to change address" and tapping it opens those calls

### Requirement: App in English or Hindi
Every screen SHALL be available in English and Hindi, switchable from any screen, and the choice SHALL be remembered on that device.

#### Scenario: Switch to Hindi
- **WHEN** the seller taps हिंदी
- **THEN** menus, labels and buttons change to Hindi and stay in Hindi next time they open the app

### Requirement: Works on a phone
Every screen SHALL be usable on a phone screen without sideways scrolling of the page.

#### Scenario: Seller on mobile
- **WHEN** the seller opens the app on a 6-inch phone
- **THEN** the menu sits at the bottom and all content fits the screen width
