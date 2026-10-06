# Spec Delta

## Purpose

The phone conversation that confirms a cash-on-delivery order with the customer and records
a clear result the seller can act on.

## ADDED Requirements

### Requirement: Opening line names the brand and the order
The agent SHALL greet the customer by name, say the brand name, the product, the amount and
"cash on delivery", tell them the call is recorded, and ask whether to ship the order.

#### Scenario: Normal opening
- **WHEN** Priya Sharma answers a call for her ₹1,299 Cotton Anarkali Kurti order from Kesar Kurtis
- **THEN** the agent says, in Hinglish, her name, "Kesar Kurtis", "Cotton Anarkali Kurti", "₹1,299" and "cash on delivery", mentions the recording, and asks if the order should be shipped

### Requirement: Customer says yes
When the customer agrees, the agent SHALL read back the delivery address and ask if it is correct, then thank them. The result SHALL be **Confirmed**.

#### Scenario: Address is correct
- **WHEN** the customer says "Haan ji, bhej dijiye" and then confirms the address
- **THEN** the agent thanks them, ends the call, and the result is Confirmed

#### Scenario: Customer gives a new address
- **WHEN** the customer says the address is wrong and says "Flat 7, Vaishali Nagar, Jaipur"
- **THEN** the agent thanks them, the result is Confirmed, and the new address is saved with the call

### Requirement: Customer says no
When the customer refuses, the agent SHALL ask the reason once, then confirm the cancellation politely. The result SHALL be **Cancelled** with the reason saved.

#### Scenario: Cancel with reason
- **WHEN** the customer says "Nahi, cancel kar dijiye" and gives the reason "galti se order ho gaya"
- **THEN** the result is Cancelled and the reason "Ordered by mistake" is saved

#### Scenario: Customer won't give a reason
- **WHEN** the customer refuses and does not want to explain
- **THEN** the agent does not insist, the result is Cancelled, and the reason is "Not given"

### Requirement: Customer is busy
When the customer asks to be called later, the agent SHALL ask for a time and confirm it back. The result SHALL be **Call later** with the requested time saved.

#### Scenario: Customer names a time
- **WHEN** the customer says "Abhi busy hoon, shaam 7 baje call karna"
- **THEN** the agent confirms "shaam 7 baje", the result is Call later, and 7:00 PM today is saved

### Requirement: Understands natural Hinglish answers
The agent SHALL understand common ways of saying yes, no and later in Hindi, English and Hinglish, not only exact words.

#### Scenario: Different ways to say yes
- **WHEN** the customer says any of "haan", "ji", "theek hai", "bhej do", "yes", "ok"
- **THEN** the agent treats it as yes

#### Scenario: Unclear answer
- **WHEN** the customer's answer is unclear two times in a row
- **THEN** the agent says the team will call again, ends the call, and the result is Call later

### Requirement: Follows the customer's language
The agent SHALL switch to Hindi or English if the customer clearly speaks in that language.

#### Scenario: Customer replies in English
- **WHEN** the agent opens in Hinglish and the customer replies "Yes, please ship it"
- **THEN** the agent continues the call in English

### Requirement: Customer can interrupt
The agent SHALL stop speaking and listen when the customer starts talking over it.

#### Scenario: Interrupting the opening
- **WHEN** the customer says "haan haan, bhej do" while the agent is still reading the order
- **THEN** the agent stops, treats it as yes, and moves to the address step

### Requirement: Replies quickly
The agent SHALL start replying within 1.5 seconds after the customer stops speaking, in at least 9 out of 10 replies.

#### Scenario: Measuring reply speed
- **WHEN** 20 test calls are reviewed
- **THEN** at least 90% of agent replies start within 1.5 seconds of the customer finishing

### Requirement: Does not make things up
The agent SHALL NOT invent answers about delivery dates, discounts, returns or anything not in the order. It SHALL say the team will get back and continue the confirmation.

#### Scenario: Off-topic question
- **WHEN** the customer asks "exchange ho jayega kya size ka?"
- **THEN** the agent says the brand's team will answer that, notes the question in the transcript, and goes back to asking about shipping

### Requirement: Handles silence and long calls
The agent SHALL ask "Hello, kya aap mujhe sun pa rahe hain?" after 8 seconds of silence, and end the call if silence continues. Calls SHALL be wrapped up politely by 3 minutes.

#### Scenario: Customer goes silent
- **WHEN** the customer says nothing for 8 seconds, twice
- **THEN** the agent ends the call politely and the result is Call later

### Requirement: Every call saves a full record
Each answered call SHALL save the result, cancel reason or new address or callback time (when given), the transcript, the recording, and the call length.

#### Scenario: Record after a confirmed call
- **WHEN** a call ends as Confirmed after 42 seconds
- **THEN** its record shows Confirmed, the 42-second length, the full transcript and a playable recording

### Requirement: Agent voice matches its gender
The agent's Hindi verb forms SHALL match the chosen voice, for example "bol rahi hoon" for a female voice and "bol raha hoon" for a male voice.

#### Scenario: Male voice
- **WHEN** the voice Rohit is used
- **THEN** the agent says "main Kesar Kurtis se Rohit bol raha hoon"
