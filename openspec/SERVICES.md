# Specs by service

Every spec, grouped by the part of HaanJi it belongs to. Specs live inside the phase that
builds them (`openspec/changes/<phase>/specs/<service>/...`). When a phase is finished and
archived, its specs move to `openspec/specs/<service>/...` automatically, in the same folders.

| Service | Spec | What it covers | Built in | Code |
|---|---|---|---|---|
| **voice** | [cod-confirmation-call](changes/add-voice-calling/specs/voice/cod-confirmation-call/spec.md) | The phone conversation and its result | Phase 1 | `backend/app/voice/` |
| **voice** | [outbound-calling](changes/add-voice-calling/specs/voice/outbound-calling/spec.md) | Placing calls, call status | Phase 1 | `backend/app/integrations/exotel.py` |
| **orders** | [order-intake](changes/add-order-calling/specs/orders/order-intake/spec.md) | COD orders from Shopify or a sheet | Phase 2 | `backend/app/shopify/` |
| **orders** | [order-result-sync](changes/add-order-calling/specs/orders/order-result-sync/spec.md) | Tags, notes, result sheet | Phase 2 | `backend/app/shopify/` |
| **scheduler** | [call-scheduling](changes/add-order-calling/specs/scheduler/call-scheduling/spec.md) | When to call, retries, callbacks | Phase 2 | `backend/app/scheduler/` |
| **dashboard** | [seller-onboarding](changes/add-seller-dashboard/specs/dashboard/seller-onboarding/spec.md) | Sign up, 4-step setup, Go live | Phase 3 | `dashboard/` |
| **dashboard** | [seller-dashboard](changes/add-seller-dashboard/specs/dashboard/seller-dashboard/spec.md) | Home screen, money saved, Hindi/English | Phase 3 | `dashboard/` |
| **dashboard** | [call-history](changes/add-seller-dashboard/specs/dashboard/call-history/spec.md) | Calls list and call detail | Phase 3 | `dashboard/` |
| **dashboard** | [call-script-editor](changes/add-seller-dashboard/specs/dashboard/call-script-editor/spec.md) | Editing what the agent says | Phase 3 | `dashboard/` |
| **dashboard** | [seller-settings](changes/add-seller-dashboard/specs/dashboard/seller-settings/spec.md) | Calling hours, voice, RTO cost, pause | Phase 3 | `dashboard/` |
| **payments** | [seller-wallet](changes/add-wallet-and-admin/specs/payments/seller-wallet/spec.md) | Balance, call charges, UPI recharge | Phase 4 | `backend/app/payments/` |
| **admin** | [admin-panel](changes/add-wallet-and-admin/specs/admin/admin-panel/spec.md) | Team view of sellers, costs, controls | Phase 4 | `dashboard/` (admin pages) |
