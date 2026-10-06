# Design: Voice calling (Phase 1)

## Context

See proposal.md for why. The project already has the COD script and conversation map in
`backend/app/voice/flow_cod.py`, and empty files for the voice pipeline and Exotel.
Nothing places real calls yet.

## Goals / Non-Goals

**Goals:** one real, natural-sounding call to a real phone, with a saved result.

**Non-Goals:** many calls at once, automatic timing, database. In this phase call records
are saved as simple JSON files (one file per call), which is enough to review calls.

## How one call works

```
Team member starts test call
        │
        ▼
Our backend ──"call this number"──► Exotel ──rings──► Customer's phone
        ▲                                │
        │       live call audio, both ways (websocket = always-open connection)
        ▼                                │
Voice pipeline:  customer audio ─► Sarvam speech-to-text ─► text
                 text + script  ─► Claude decides: yes / no / later / unclear
                 next script line ─► Sarvam text-to-speech ─► audio back to customer
        │
        ▼
Call ends ─► result + transcript + recording saved
```

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Phone provider | Exotel | Indian numbers and live audio streaming; Plivo as backup |
| Voice framework | Pipecat (open source) | Handles interruptions and audio timing; supports Exotel and Sarvam |
| Speech to text, text to speech | Sarvam AI | Built for Hindi and Hinglish, Indian accents |
| AI model | Claude Haiku 4.5 | Fast, which matters most on a live call |
| Who decides the next line | Script map in `flow_cod.py`; Claude only picks the customer's intent and extracts details (reason, time, address) | The agent can't go off-script or invent answers |
| Where it runs while testing | Founder's laptop + ngrok (a tool that gives the laptop a public web address) | No server cost until it works |
| Where call records go | JSON files in a `recordings/` folder | Database comes in Phase 2 |

Other options considered: an all-in-one voice platform (Bolna, Vapi) is faster to start but
costs more per call and gives less control. We can switch to one if Phase 1 gets stuck.

## Risks / Trade-offs

- [Replies feel slow] → Keep Claude prompts short, use streaming, aim for ~1 second; measure on 20 calls.
- [Hinglish misheard on bad networks] → Ask again once, then end as Call later (never guess).
- [Exotel KYC takes long] → Start KYC now; build against Exotel's test setup meanwhile.
- [Cost per call too high for ₹3 price] → Log the cost of every test call; target under ₹1.50.

## Open Questions

- Which exact Sarvam voices map to the names Ananya, Meera, Rohit and Kabir. Can be picked
  after listening, without changing anything else.
