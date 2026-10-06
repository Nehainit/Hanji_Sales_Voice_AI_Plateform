# Proposal: Seller dashboard (Phase 3)

## Why

In Phase 2 the founder sets up every store by hand and sellers can't see their calls.
To grow beyond a few pilots, sellers with no technical knowledge must be able to sign up,
set up, see results and change their script on their own, in Hindi or English.

## What Changes

- A web app (works on phone and laptop) that matches the clickable prototype in
  `dashboard/prototype/`.
- Sign up with Google or a mobile OTP (one-time password sent by SMS).
- A 4-step setup: connect store, pick language, pick voice, test call, then **Go live**.
- A home screen showing money saved, today's calls and what needs attention.
- A calls list with filters, search, transcript and recording for every call.
- A simple script editor (plain text boxes, no flowcharts) with a live preview.
- Settings for calling hours, retries, voice, language and RTO cost.
- The whole app can be switched between English and Hindi.

## Capabilities

### New Capabilities
- `dashboard/seller-onboarding`: sign up, the 4-step setup, test call and going live.
- `dashboard/seller-dashboard`: the home screen: money saved, today's numbers, 7-day chart, attention list, app language.
- `dashboard/call-history`: the list of calls and the detail of each call.
- `dashboard/call-script-editor`: changing what the agent says.
- `dashboard/seller-settings`: calling hours, retries, voice, language, order sources, RTO cost, pausing calls.

### Modified Capabilities
- None.

## Out of scope

- Wallet, recharge and the admin panel (Phase 4)
- Team member logins and roles (Version 2)
- Drag-and-drop flow builder and "describe it and AI builds it" (later)
- WhatsApp follow-up when a call isn't answered (Version 2)

## Impact

- New Next.js app in `dashboard/`, using Supabase for login and data.
- New backend endpoints for the screens (calls list, script, settings, test call).
- Phase 2's manual store setup is replaced by self-serve setup.
