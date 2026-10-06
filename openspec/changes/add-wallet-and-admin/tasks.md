# Tasks

## 1. Setup (founder)

- [ ] 1.1 Complete Razorpay KYC and get test and live API keys; done when both key pairs are in `.env`
- [ ] 1.2 Add a prices setting (₹3 first minute, ₹2 each extra minute); done when the admin panel can read the current prices

## 2. Wallet basics

- [x] 2.1 Calculate balance as the sum of a seller's wallet rows; done when a test with +₹150, −₹3, −₹5 shows ₹142
- [ ] 2.2 Give ₹150 free credit on sign-up, once; done when a new test account shows ₹150 and signing in again does not add more
- [x] 2.3 Charge answered calls by length; done when tests show 42 seconds costs ₹3, 1 minute 20 seconds costs ₹5, and unanswered and test calls cost ₹0
- [ ] 2.4 Block double charging; done when saving the same call result twice leaves only one charge
- [ ] 2.5 Reserve ₹3 before dialling and release it if not answered; done when 10 calls started at once with ₹15 balance never take the balance below zero

## 3. Adding money

- [ ] 3.1 Build the wallet screen (balance, calls left, price rule, amounts); done when ₹1,840 shows "≈ 613 calls left"
- [ ] 3.2 Connect Razorpay UPI checkout in test mode; done when a test payment opens the UPI screen
- [ ] 3.3 Add money only on Razorpay's signed "payment captured" message; done when a test payment raises the balance within 1 minute and a fake message with a wrong signature is refused
- [ ] 3.4 Show the failed-payment message; done when cancelling a test payment leaves the balance unchanged and shows "Payment didn't go through"
- [ ] 3.5 Add the check for missed Razorpay payments every few minutes; done when a payment made while the backend was off is added after restart

## 4. Alerts and running out

- [ ] 4.1 Show the low balance warning and send one SMS a day below ₹300; done when dropping a test wallet to ₹297 shows the warning and sends exactly one SMS that day
- [ ] 4.2 Pause calls when the balance can't cover a call; done when a ₹2 test wallet places no calls
- [ ] 4.3 Call waiting orders after recharge (if under 24 hours old); done when 15 waiting test orders are all called after adding ₹1,000
- [ ] 4.4 Show wallet history with call charges grouped by day; done when yesterday's calls show as one line

## 5. Admin panel

- [ ] 5.1 Add the team-only check on every admin page and request; done when a seller account gets "You don't have access" and no data
- [ ] 5.2 Build the sellers list with status, balance, calls today and search; done when searching "Kesar" finds Kesar Kurtis with the right numbers
- [ ] 5.3 Save the real cost of each call (phone, speech, AI); done when a test call's record shows its cost split into the three parts
- [ ] 5.4 Build the cost and margin view per day and per seller, highlighting margin under 30%; done when test data of ₹3,200 earned and ₹1,350 cost shows ₹1,850 margin
- [ ] 5.5 Add free credit with a required reason and a log; done when a credit without a reason is refused and one with a reason shows who, when and why
- [ ] 5.6 Add pause and resume by the team; done when a team-paused seller sees "Calling paused by HaanJi support" and cannot resume it
- [ ] 5.7 Build the failed calls list for the last 7 days; done when test failures appear with seller, time and error

## 6. Final check

- [ ] 6.1 Switch Razorpay to live mode and make one real ₹500 recharge; done when the money arrives in the Razorpay account and the wallet shows +₹500
- [ ] 6.2 Run one week with all pilot sellers on paid wallets; done when every answered call has exactly one charge and the margin view matches Exotel, Sarvam and Anthropic bills within 5%
