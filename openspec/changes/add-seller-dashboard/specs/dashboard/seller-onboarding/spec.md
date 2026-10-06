# Spec Delta

## Purpose

Letting a seller with no technical knowledge create an account, connect their orders, choose
how calls sound, hear a test call and go live in about five minutes, on their own.

## ADDED Requirements

### Requirement: Sign up with Google or mobile OTP
A seller SHALL be able to sign up or log in with a Google account or with an Indian mobile number and a one-time password sent by SMS. The password SHALL work for 5 minutes only.

#### Scenario: Mobile sign-up
- **WHEN** a seller enters 98290 41122 and types the OTP within 5 minutes
- **THEN** their account is created and the setup starts

#### Scenario: OTP too late
- **WHEN** the seller types the OTP after 6 minutes
- **THEN** they see "This OTP has expired. Tap Resend to get a new one."

### Requirement: Step 1, connect where orders come from
The seller SHALL connect a Shopify store with one button, or upload an order sheet. They SHALL NOT move to step 2 until one of these is done.

#### Scenario: Shopify connected
- **WHEN** the seller enters kesarkurtis.myshopify.com and approves the app in Shopify
- **THEN** they see "Connected" with how many orders and what share were COD in the last 30 days, and Next is enabled

### Requirement: Step 2, pick the call language
The seller SHALL choose Hinglish, Hindi or English, with Hinglish selected by default. Languages not yet available SHALL be shown as "Coming soon" and cannot be picked.

#### Scenario: Tamil not ready
- **WHEN** the seller taps Tamil
- **THEN** nothing is selected and it stays marked "Coming soon"

### Requirement: Step 3, pick a voice by listening
The seller SHALL choose one of four voices (Ananya, Meera, Rohit, Kabir) and hear a sample of each, using their own brand name, before choosing.

#### Scenario: Listening to Rohit
- **WHEN** the seller taps play on Rohit
- **THEN** they hear Rohit say the opening line with "Kesar Kurtis" in it

### Requirement: Step 4, test call on the seller's own phone
The seller SHALL be able to get a real test call on their own number with a sample order, and try every answer. The test call SHALL be free and SHALL NOT appear in their real call numbers.

#### Scenario: Seller tries "cancel"
- **WHEN** the seller takes the test call and says "nahi, cancel karo"
- **THEN** the agent asks the reason, the call ends as Cancelled, and the screen shows the result as it would appear in their calls list

### Requirement: Nothing is called before Go live
The system SHALL NOT call any real customer of the seller until the seller presses **Go live**.

#### Scenario: Setup left halfway
- **WHEN** a seller connects Shopify but never presses Go live, and 30 COD orders come in
- **THEN** none of those customers are called
