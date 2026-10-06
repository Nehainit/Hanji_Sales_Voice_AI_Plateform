# Tasks

## 1. Setup

- [x] 1.1 Create the Next.js app in `dashboard/` with the prototype's colours and fonts; done when the empty app opens in a browser in HaanJi colours
- [x] 1.2 Add English and Hindi text files and the language switch; done when switching to हिंदी changes the menu labels and is remembered after reload
- [ ] 1.3 Start DLT registration for OTP SMS (founder); done when the SMS sender ID is approved
- [ ] 1.4 Turn on row-level security in Supabase; done when a test proves seller A cannot read seller B's calls

## 2. Sign up and setup

- [ ] 2.1 Add Google login; done when a new Google account lands on setup step 1
- [ ] 2.2 Add mobile OTP login with 5-minute expiry; done when an OTP typed after 6 minutes shows the expiry message
- [ ] 2.3 Build step 1 (Shopify connect or sheet upload); done when Next stays disabled until one is done
- [ ] 2.4 Build step 2 (language) with "Coming soon" languages; done when Tamil cannot be selected
- [ ] 2.5 Build step 3 (voices) with samples using the seller's brand name; done when each play button speaks the opening with the brand name
- [ ] 2.6 Build step 4 (test call to own phone); done when the seller's phone rings, the result shows on screen, and it does not count in their numbers
- [ ] 2.7 Add Go live; done when a store that hasn't gone live gets no customer calls, and calls start after pressing it

## 3. Home screen

- [ ] 3.1 Show money saved this month with the calculation below; done when 293 test cancellations at ₹160 show ₹46,880
- [ ] 3.2 Show today's four numbers; done when they match a count of today's calls in the database
- [ ] 3.3 Add the 7-day chart with legend, tap details and table view; done when tapping a day shows its three counts and the table matches the chart
- [ ] 3.4 Add the "Needs your attention" list with links; done when a new-address call appears there and tapping opens it
- [ ] 3.5 Check the home screen on a phone in both languages; done when nothing overflows sideways

## 4. Calls

- [ ] 4.1 Build the calls list, newest first, with masked phone numbers; done when no full number is visible in the list
- [ ] 4.2 Add result filters with counts and search; done when "Cancelled" + "Jaipur" shows only those calls, and an empty search shows the "No calls match" message
- [ ] 4.3 Build the call detail with transcript and recording player; done when a test call's recording plays from the detail screen
- [ ] 4.4 Add the daily 90-day cleanup; done when a test call dated 100 days ago shows "Recording deleted after 90 days"

## 5. Script editor

- [ ] 5.1 Build the editor with the six lines and two switches; done when switching off the address check skips it on the next test call
- [ ] 5.2 Add tap-to-insert details and the live preview; done when typing "Shukriya {name} ji!" previews "Shukriya Priya ji!"
- [ ] 5.3 Add save checks (empty, over 300 characters, unknown details); done when {nam} shows the "Did you mean {name}?" message
- [ ] 5.4 Apply saved scripts only to new calls; done when a call in progress during save keeps the old lines
- [ ] 5.5 Always speak the recording notice; done when a script without it still says it on a test call
- [ ] 5.6 Add test call and reset to default; done when reset brings back the standard lines

## 6. Settings

- [ ] 6.1 Build calling time settings with the start-before-end check; done when 10 AM–8 PM makes a 9:30 AM order wait until 10:00 AM
- [ ] 6.2 Add voice and language settings; done when changing to Meera makes the next test call use Meera
- [ ] 6.3 Add order sources (Shopify status, disconnect, sheet upload); done when disconnecting cancels planned calls
- [ ] 6.4 Add RTO cost; done when changing it to ₹200 updates money saved
- [ ] 6.5 Add pause and resume; done when 20 orders received while paused are all called after resuming

## 7. Final check

- [ ] 7.1 Have 3 sellers who have never seen HaanJi sign up and go live alone while you watch; done when each one finishes setup in under 10 minutes without help
