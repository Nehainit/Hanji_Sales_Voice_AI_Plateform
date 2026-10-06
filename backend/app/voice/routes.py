"""Phase 1: HTTP/websocket endpoints Exotel connects to during a call.

TODO (Phase 1):
- WebSocket endpoint that Exotel's Voicebot applet streams call audio to;
  hand the socket to pipeline.py.
- Status-callback endpoint Exotel hits when a call ends (answered / busy /
  no-answer) so the scheduler can plan a retry.
- Register this router in app/main.py.
"""
