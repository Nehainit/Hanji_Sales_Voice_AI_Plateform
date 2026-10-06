# Proposal: Order calling (Phase 2)

## Why

After Phase 1, the agent can hold a good call, but someone has to start each call by hand.
Sellers need it to happen on its own: a new COD order comes in, the customer gets a call at
the right time, and the result shows up on the order. This is what makes the first pilot
brand possible.

## What Changes

- New COD orders arrive automatically from Shopify. Prepaid orders are ignored.
- Sellers without Shopify can upload an Excel or CSV sheet of orders instead.
- Each order gets its first call a few minutes after it is placed, only inside calling hours.
- Unanswered calls are retried automatically, and "call me later" requests are honoured.
- After each call, the result is written back: a tag and a note on the Shopify order, or a
  downloadable result sheet for uploaded orders.
- Orders, calls and results are saved in a database (Supabase) instead of files.

## Capabilities

### New Capabilities
- `orders/order-intake`: getting COD orders in, from Shopify or an uploaded sheet.
- `scheduler/call-scheduling`: deciding when each call happens: delay, calling hours, retries, callbacks.
- `orders/order-result-sync`: sending each call's result back to Shopify or into a result sheet.

### Modified Capabilities
- None.

## Out of scope

- Cancelling the order in Shopify automatically (we only tag it; the seller decides)
- Changing the address in Shopify automatically (we flag it for the seller)
- WooCommerce, Shiprocket and other platforms (Version 2)
- Seller dashboard (Phase 3) and wallet charges (Phase 4)
- A public Shopify App Store listing; pilot stores use a private "custom app"

## Impact

- New code in `backend/app/shopify/`, `backend/app/scheduler/` and `backend/app/integrations/supabase.py`.
- Uses the existing calling rules in `backend/app/scheduler/rules.py`.
- Database tables from `database/schema.sql` go live in Supabase.
- Needs accounts: Shopify Partner, Supabase, Redis.
