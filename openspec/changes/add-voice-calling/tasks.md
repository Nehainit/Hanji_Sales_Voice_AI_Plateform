# Tasks

## 1. Accounts and keys (founder)

- [ ] 1.1 Sign up on Exotel and submit KYC; done when an ExoPhone number shows in the Exotel dashboard
- [ ] 1.2 Get a Sarvam AI API key and an Anthropic API key; done when both are pasted into `.env`
- [ ] 1.3 Install ngrok and get a public URL; done when `PUBLIC_BASE_URL` in `.env` is filled
- [ ] 1.4 Open `http://localhost:8000/health` with the backend running; done when `phase1_keys_missing` is an empty list

## 2. Placing a call

- [x] 2.1 Add phone number cleaning (+91, spaces, leading 0) to `voice/outbound-calling`; done when tests show "+91 98290 41122" becomes 9829041122 and "98290 411" is rejected
- [ ] 2.2 Write `integrations/exotel.py` to start a call; done when running it rings the founder's phone (silent call is fine)
- [ ] 2.3 Add the call-ended endpoint that saves Answered / Busy / Not answered / Failed; done when an unanswered test call shows "Not answered" in its record
- [x] 2.4 Block a second call to a number already on a call; done when a test shows the second request is refused

## 3. The conversation

- [ ] 3.1 Connect Exotel's live audio to a Pipecat pipeline that only repeats a fixed Hinglish greeting; done when the founder hears the greeting on their phone
- [ ] 3.2 Add Sarvam speech-to-text and log what the customer said; done when the founder's spoken "haan ji" appears in the log
- [ ] 3.3 Add Claude intent detection (yes / no / later / unclear + reason, time, address); done when tests pass for 10 sample Hinglish answers, including "theek hai", "mat bhejo", "shaam ko karna"
- [ ] 3.4 Walk the script map in `flow_cod.py` and speak each line with Sarvam text-to-speech; done when a test call can reach Confirmed, Cancelled and Call later
- [ ] 3.5 Add the recording notice to the opening line; done when every test call says it within the first sentence
- [ ] 3.6 Turn on interruptions; done when saying "haan haan" over the opening jumps straight to the address step
- [ ] 3.7 Add silence handling (8 seconds, then once more) and the 3-minute limit; done when staying silent on a test call ends it as Call later
- [ ] 3.8 Add language switching; done when replying in English makes the agent continue in English
- [ ] 3.9 Add the "team will answer that" reply for off-topic questions; done when asking about size exchange gets that reply and the call continues

## 4. Saving and testing

- [ ] 4.1 Save each call as a JSON file with result, details, transcript, recording link and length; done when a test call's file contains all of these
- [ ] 4.2 Add a "start test call" command that uses the sample order; done when the founder can run it with one command and their phone rings
- [ ] 4.3 Log time-to-reply for each agent turn; done when the call file shows reply times in seconds

## 5. Final check

- [ ] 5.1 Make 20 test calls (different people, both genders of voice, good and bad network); done when at least 90% of replies start within 1.5 seconds and every call ends with the right result
- [ ] 5.2 Note the real cost of each test call (Exotel + Sarvam + Claude); done when the average cost per call is written in `docs/roadmap.md`
