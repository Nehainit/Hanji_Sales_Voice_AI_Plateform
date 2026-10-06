# Proposal: Voice calling (Phase 1)

## Why

The whole product depends on one thing: a phone call that sounds natural in Hinglish and
correctly understands "haan", "nahi" or "baad mein". This is the hardest and riskiest part,
so we build and prove it first, before Shopify, dashboards or payments.

## What Changes

- The system can phone an Indian mobile number from our business number.
- On the call, an AI agent reads out the order, asks the customer to confirm, and follows
  the COD script: confirm the address, ask the cancel reason, or ask when to call back.
- Every call ends with one clear result: **Confirmed**, **Cancelled**, **Call later** or
  **No answer**, plus the transcript (written record of the call) and the recording.
- A team member can start a test call with a sample order to any phone, to hear and judge it.

## Capabilities

### New Capabilities
- `voice/cod-confirmation-call`: the conversation itself: what the agent says, how it understands
  the customer, and what result it records.
- `voice/outbound-calling`: placing a phone call to a customer and reporting what happened
  (answered, busy, not answered, failed).

### Modified Capabilities
- None.

## Out of scope

- Shopify orders, automatic call timing and retries (Phase 2)
- Seller dashboard and script editing (Phase 3)
- Wallet and payments (Phase 4)
- Customers calling back on our number, WhatsApp messages, regional languages
  (Tamil, Telugu and others)

## Impact

- New code in `backend/app/voice/` and `backend/app/integrations/exotel.py`.
- Uses the existing script in `backend/app/voice/flow_cod.py`.
- Needs accounts and keys: Exotel, Sarvam AI, Anthropic (see `docs/services-checklist.md`).
