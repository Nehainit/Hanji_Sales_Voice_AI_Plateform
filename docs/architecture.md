# Architecture

```
Shopify ──orders/create──► backend/shopify/webhooks.py
                                   │ save order, queue first call
                                   ▼
                           Redis queue ◄── scheduler/rules.py (delay, hours, retries)
                                   │
                                   ▼
                           scheduler/worker.py ──place_call──► Exotel ──► customer's phone
                                                                  │
                                              call audio (websocket)
                                                                  ▼
                           voice/routes.py ──► voice/pipeline.py
                                                 Sarvam STT → Claude → Sarvam TTS
                                                 follows voice/flow_cod.py
                                   │
                                   ▼ outcome + transcript + recording
                 Supabase (database/schema.sql)  +  shopify/tags.py (order tag)
                                   │
                                   ▼
                           dashboard/ (seller sees calls, money saved, wallet)
```

## One order, start to finish

1. Customer places a COD order on Shopify.
2. Shopify sends `orders/create` to our webhook. We save the order and queue a call
   at `first_call_time()` (5 min later, inside 9 AM–9 PM).
3. The worker checks the seller's wallet, then asks Exotel to call the customer.
4. Exotel streams the call audio to our websocket. The pipeline listens (Sarvam STT),
   decides the reply (Claude, following `flow_cod.FLOW`) and speaks (Sarvam TTS).
5. The call ends at an outcome: confirmed / cancelled / callback.
   If nobody answers, `next_retry_time()` schedules another try (max 3).
6. We save the transcript and recording, tag the Shopify order (`cod-confirmed` etc.)
   and charge the wallet ₹3 for an answered call.

## Hosting

Everything runs in AWS Mumbai (ap-south-1) to keep voice latency low.
