# Design: Wallet and admin panel (Phase 4)

## Context

See proposal.md for why. The `wallet_transactions` table already exists in
`database/schema.sql`. Calls, results and seller accounts come from Phases 1–3.

## Goals / Non-Goals

**Goals:** charge correctly for every answered call, take UPI top-ups, give the team one safe
control room.

**Non-Goals:** GST invoices, refunds to bank, monthly plans.

## How money moves

```
Seller taps "Pay ₹2,000" ─► Razorpay UPI screen ─► seller pays in their UPI app
                                    │
                    Razorpay tells our backend "payment captured" (webhook, signature checked)
                                    ▼
                    wallet_transactions: +₹2,000 "recharge"

Call answered, 1 min 20 s ─► wallet_transactions: −₹5 "call_charge"
Balance = sum of all rows for that seller
```

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Money unit | Whole paise (₹3 = 300) | No rounding mistakes |
| Balance | Always the sum of the seller's wallet rows; rows are never edited or deleted | Every rupee can be traced; mistakes are fixed with a new row |
| Charging moment | When the call record is saved as answered | Free for unanswered calls by design |
| Same call charged twice | One charge row per call, enforced by the database | Retries or crashes can't double-charge |
| Recharge confirmation | Only Razorpay's signed "payment captured" message adds money, not the browser | A seller can't fake a payment from their browser |
| Payment method | Razorpay, UPI only | Most Indian sellers prefer UPI; fewer screens |
| Prices | Stored in a settings table, read at charge time | Team can change prices without new code |
| Admin access | A `is_team` flag on accounts, checked by the backend on every admin request | Hiding the link is not enough |
| Admin actions log | Every credit and pause saves who, when and why | Accountability and easy support |
| Cost tracking | Each call saves its real cost from Exotel, Sarvam and Claude usage | Needed for the margin view |

## Risks / Trade-offs

- [Balance check and call happen at the same moment for many orders] → Reserve ₹3 before dialling; release it if the call is not answered.
- [Razorpay message arrives late] → Show "Payment received, updating balance" and refresh when it lands; also check Razorpay every few minutes for missed payments.
- [Call costs rise above ₹3] → Margin view highlights any day where margin falls under 30%.

## Open Questions

- The exact low-balance SMS text. Can be written later without changing the design.
