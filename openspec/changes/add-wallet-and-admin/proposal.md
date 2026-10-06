# Proposal: Wallet and admin panel (Phase 4)

## Why

Sellers can now set up and use HaanJi on their own, but there is no way to charge them,
and the team has no single place to watch accounts, costs and problems. Without these we
cannot earn money or run many sellers safely.

## What Changes

- Every seller has a prepaid wallet (money added in advance, used up by calls).
- New sellers get 50 free calls (₹150 credit).
- Only answered calls cost money: ₹3 for up to 1 minute, ₹2 for each extra minute.
  Unanswered, busy, failed and test calls are free.
- Sellers add money by UPI through Razorpay (a payment company).
- Low balance alerts, and calls pause (not lost) when the balance runs out.
- An admin panel for the HaanJi team: all sellers, usage, costs, margin, free credit,
  pausing an account, and failed calls.

## Capabilities

### New Capabilities
- `payments/seller-wallet`: balance, call charges, free credit, UPI recharge, alerts and history.
- `admin/admin-panel`: the team's view of all sellers, costs and problems, with safe controls.

### Modified Capabilities
- None. (The wallet balance shown in the dashboard's attention list was already specified
  in Phase 3; this change provides the real balance.)

## Out of scope

- Monthly plans, invoices with GST details and refunds to bank (later)
- Card or net-banking payments (UPI only to start)
- Agency or reseller accounts (later)

## Impact

- New code in `backend/app/payments/`, wallet and admin screens in `dashboard/`.
- Uses the `wallet_transactions` table from `database/schema.sql`.
- Needs a Razorpay account with completed KYC.
