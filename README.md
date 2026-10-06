# HaanJi — COD order confirmation voice agent

HaanJi calls Indian D2C customers in Hindi/Hinglish/English a few minutes after they place a
cash-on-delivery order, confirms the order (or cancels / reschedules it), and tags the result
back in Shopify. Goal: cut RTO (return-to-origin) losses for sellers.

> "HaanJi" is a working name. The clickable prototype lives in `dashboard/prototype/`.

## Folder structure

```
voice_development/
├── README.md               ← you are here
├── .env.example            ← every API key the project needs, grouped by phase
├── docs/
│   ├── architecture.md     ← how the pieces talk to each other
│   ├── services-checklist.md ← accounts to create + documents needed
│   └── roadmap.md          ← build phases and "done" criteria
├── backend/                ← our Python code (FastAPI)
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py         ← starts the server
│   │   ├── config.py       ← reads keys from .env
│   │   ├── voice/          ← Phase 1: the phone conversation
│   │   │   ├── flow_cod.py ← what the agent says, and where each answer leads
│   │   │   ├── pipeline.py ← speech-to-text → Claude → text-to-speech (Pipecat)
│   │   │   └── routes.py   ← websocket Exotel streams call audio to
│   │   ├── scheduler/      ← Phase 2: when to call, retries, calling hours
│   │   │   ├── rules.py
│   │   │   └── worker.py
│   │   ├── shopify/        ← Phase 2: new-order webhooks, order tags
│   │   ├── orders/         ← Phase 2: order sheet upload and row checks
│   │   ├── phone.py        ← cleans customer phone numbers
│   │   ├── payments/       ← Phase 4: Razorpay wallet recharge
│   │   └── integrations/   ← clients for outside services (Exotel, Supabase)
│   └── tests/
├── database/
│   └── schema.sql          ← all tables (Supabase / Postgres)
└── dashboard/              ← Phase 3: seller web app (Next.js)
    └── prototype/          ← clickable HTML prototype, the design reference
```

## Which outside service lives where

| Service | Used for | Code |
|---|---|---|
| Exotel (or Plivo) | Indian phone number, placing calls, streaming audio | `backend/app/integrations/exotel.py`, `backend/app/voice/routes.py` |
| Sarvam AI | Hindi speech-to-text and text-to-speech | `backend/app/voice/pipeline.py` |
| Anthropic (Claude) | Deciding what the agent says next | `backend/app/voice/pipeline.py` |
| Shopify | New COD orders in, result tags out | `backend/app/shopify/` |
| Supabase | Database, seller login, call recordings | `backend/app/integrations/supabase.py`, `database/schema.sql` |
| Redis | Queue of calls waiting to go out | `backend/app/scheduler/` |
| Razorpay | UPI wallet recharge | `backend/app/payments/` |

## Running the backend (local)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env      # then fill in the keys you have
uvicorn app.main:app --reload   # open http://localhost:8000/health
pytest                          # run the tests
```

## Status

- [x] Niche chosen, feature set defined, clickable prototype
- [x] Project structure, calling rules (`scheduler/rules.py`), COD flow (`voice/flow_cod.py`), DB schema
- [x] Spec documents for all 4 phases in `openspec/changes/` (OpenSpec)
- [ ] Phase 1 — first real call to your own phone (`openspec/changes/add-voice-calling/tasks.md`)

## Specs (OpenSpec)

Each phase is one OpenSpec change with four simple documents:
`proposal.md` (what and why), `specs/` (what the product must do, with examples),
`design.md` (how it will be built) and `tasks.md` (checklist, each task says how to check it's done).

| Phase | Folder |
|---|---|
| 1. Voice calling | `openspec/changes/add-voice-calling/` |
| 2. Order calling (Shopify, timing, retries) | `openspec/changes/add-order-calling/` |
| 3. Seller dashboard | `openspec/changes/add-seller-dashboard/` |
| 4. Wallet and admin panel | `openspec/changes/add-wallet-and-admin/` |

Inside each phase, specs are grouped by service (`voice/`, `orders/`, `scheduler/`, `dashboard/`,
`payments/`, `admin/`). `openspec/SERVICES.md` lists every spec by service in one table.

Useful commands: `openspec list` (progress), `openspec view` (dashboard), `openspec validate --all`.
