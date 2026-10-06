"""Phase 1: the live conversation pipeline (Pipecat).

Audio from Exotel → Sarvam speech-to-text → Claude (decides the reply,
following flow_cod.FLOW) → Sarvam text-to-speech → audio back to Exotel.

TODO (Phase 1):
- Build a Pipecat pipeline with the Exotel websocket serializer as transport.
- Sarvam STT (Hindi/Hinglish) and Sarvam TTS (voice chosen by the seller).
- Claude (settings.claude_model) classifies each customer reply into the
  intents in flow_cod.FLOW and speaks the next node's line.
- Allow barge-in (customer can interrupt the agent).
- On reaching an "end" node, return the outcome + transcript to the caller.
- Target: under ~1s from customer stops speaking to agent starts replying.
"""
