# Design: Seller dashboard (Phase 3)

## Context

See proposal.md for why. The prototype in `dashboard/prototype/haanji-prototype.html`
already shows every screen, label and flow in English and Hindi. The backend from Phases 1–2
holds orders, calls and results in Supabase.

## Goals / Non-Goals

**Goals:** make the prototype real, connected to real data, for sellers to use without help.

**Non-Goals:** wallet screens (Phase 4), team logins, admin panel.

## How the pieces fit

```
Seller's phone / laptop
        │
        ▼
Next.js web app (dashboard/) ── login ──► Supabase Auth (Google + SMS OTP)
        │
        ├── reads calls, orders, stats ──► Supabase database (each seller sees only their own rows)
        │
        └── actions (save script, settings, test call, go live) ──► our backend (FastAPI)
                                                                     │
                                                                     └─► voice + scheduler (Phases 1–2)
```

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Web app framework | Next.js | Common, easy to hire for, works well on phones |
| Login | Supabase Auth with Google and SMS OTP | Already in our stack; no password to forget |
| SMS for OTP | An Indian SMS provider with DLT registration (the TRAI sender registration) | Required for SMS in India |
| Data access | Supabase row-level security (each seller can only read their own rows) | A bug in the app can't leak another seller's calls |
| Actions | Go through our backend, not straight to the database | Keeps the rules (calling hours, scripts) in one place |
| Translations | One English and one Hindi text file; every label comes from them | Same approach as the prototype; easy to add languages |
| Design | Copy colours, fonts and layout from the prototype | Already shown to sellers |
| Recordings | Stored in Supabase Storage; links that expire after a few minutes | Recordings can't be shared by copying a link |
| 90-day cleanup | Daily job deletes recordings and transcripts older than 90 days | Matches the spec; less personal data kept |

## Risks / Trade-offs

- [Hindi text is longer and breaks layouts] → Check every screen in Hindi on a phone before release.
- [DLT registration for OTP SMS takes time] → Start registration at the start of this phase; Google login works meanwhile.
- [Money saved looks wrong to the seller] → Always show the calculation under the number.
- [Script edits make the agent sound odd] → Live preview + test call before save; reset to default.

## Open Questions

- Which SMS provider to use for OTP. Any DLT-registered provider fits this design.
