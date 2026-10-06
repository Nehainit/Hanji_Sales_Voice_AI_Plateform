"""Phase 2: receives Shopify webhooks.

TODO (Phase 2):
- orders/create: verify the HMAC signature, keep only COD orders, save the
  order, queue the first call at rules.first_call_time().
- orders/cancelled: drop any pending calls for that order.
- app/uninstalled: stop calling for that store.
"""
