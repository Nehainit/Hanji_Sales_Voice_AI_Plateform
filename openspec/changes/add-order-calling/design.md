# Design: Order calling (Phase 2)

## Context

See proposal.md for why. Phase 1 gives us a working call. `scheduler/rules.py` already works
out first-call and retry times (tested). `database/schema.sql` has the tables we need.

## Goals / Non-Goals

**Goals:** order in → call at the right time → result back on the order, with no manual step.

**Non-Goals:** seller screens (Phase 3), charging the wallet (Phase 4). In this phase the
founder sets up each pilot store by hand.

## How one order flows

```
Shopify "new order" message (webhook) ─► check it's really from Shopify, COD only
        │                                  save order (skip if already saved)
        ▼
rules.first_call_time() ─► put a "call job" in the queue (Redis) for 10:05 AM
        │
        ▼ at 10:05 AM
Worker picks the job ─► order still open? ─► place call (Phase 1)
        │
        ▼ call ends
Save result ─► tag + note on Shopify order
        │
        └─ not answered? ─► rules.next_retry_time() ─► new job in the queue
```

## Decisions

| Decision | Choice | Why |
|---|---|---|
| How orders arrive | Shopify webhooks (Shopify sends us a message on each new order) | Instant; no need to keep checking the store |
| Checking a message is real | Verify Shopify's signature on every webhook | Stops fake orders being injected |
| Spotting COD | Order's payment method is "Cash on Delivery (COD)" | This is how Shopify marks COD |
| Pilot store setup | One Shopify "custom app" per pilot store | No App Store review needed to start |
| Call queue | Redis with jobs keyed by order + try number | Survives restarts; a job can't be added twice |
| Database | Supabase (hosted Postgres) | Free to start; also gives login and file storage later |
| Sheet upload | CSV and .xlsx, checked row by row before saving | Sellers fix problems before any call |
| Times | Everything stored in IST-aware time | Calling hours are Indian local time |

## Risks / Trade-offs

- [Webhook missed while our server is down] → Every 15 minutes, fetch the last hour's orders from Shopify and add any we missed (duplicates are ignored).
- [Many orders at once, e.g. a sale] → Limit how many calls run at the same time; the rest wait a few minutes in the queue.
- [Order cancelled in Shopify just before the call] → Worker re-checks the order is still open right before dialling.
- [Phone formats in sheets are messy] → Reuse the Phase 1 number cleaning; show bad rows clearly.

## Open Questions

- How many calls can run at the same time on our Exotel plan. Only changes a number in
  settings, not the design.
