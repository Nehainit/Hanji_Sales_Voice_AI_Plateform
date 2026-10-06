# Tasks

## 1. Accounts and setup (founder)

- [ ] 1.1 Create a Shopify Partner account and a free development store; done when you can place a test COD order in it
- [x] 1.2 Create a Supabase project and run `database/schema.sql` in its SQL editor; done when the tables show in Supabase's Table Editor
- [x] 1.3 Install Redis locally; done when the backend health check reports Redis as reachable

## 2. Database

- [x] 2.1 Write `integrations/supabase.py` with save-order, save-call and update-order functions; done when a test saves a sample order and reads it back
- [ ] 2.2 Move Phase 1 call records from JSON files into the `calls` table; done when a test call appears as a row in Supabase

## 3. Getting orders in

- [ ] 3.1 Create the custom app for the development store and connect it; done when the store shows the app as installed
- [ ] 3.2 Add the new-order webhook with signature check; done when a test COD order appears in the `orders` table within 1 minute, and a request with a wrong signature is refused
- [ ] 3.3 Ignore prepaid orders; done when a test prepaid order does not appear in `orders`
- [ ] 3.4 Ignore repeated messages for the same order; done when sending the same order twice leaves one row and one planned call
- [ ] 3.5 Mark orders with missing or invalid phones as "Can't call"; done when a test order without a phone is saved with that status and no call is planned
- [x] 3.6 Add sheet upload with row-by-row checks; done when a 50-row test sheet with 2 bad rows reports "48 orders ready" and names rows 5 and 9
- [x] 3.7 Add "Start calling" for uploaded sheets; done when no calls are planned until it is pressed
- [ ] 3.8 Handle app uninstall; done when uninstalling the app cancels all planned calls for that store
- [ ] 3.9 Add the 15-minute catch-up check for missed orders; done when an order created while the backend was off gets picked up after restart

## 4. Calling at the right time

- [x] 4.1 Plan the first call with `rules.first_call_time()`; done when a test order at 8:58 PM gets a call planned for 9:00 AM next day
- [ ] 4.2 Write `scheduler/worker.py` to place due calls; done when a planned call actually rings the test phone at the planned minute
- [ ] 4.3 Re-check the order is still open before dialling; done when cancelling the order in Shopify before its call time means no call
- [x] 4.4 Plan retries with `rules.next_retry_time()`; done when not answering three times leaves the order as No answer with no fourth call
- [ ] 4.5 Plan callbacks at the customer's time; done when saying "shaam 7 baje" on a test call plans the next call for 7:00 PM
- [x] 4.6 Limit how many calls run at once (setting, start with 5); done when 20 test orders at once never have more than 5 calls running

## 5. Sending results back

- [ ] 5.1 Write `shopify/tags.py` to set exactly one HaanJi tag; done when a callback-then-confirmed test order ends with only `cod-confirmed`
- [ ] 5.2 Add the order note with reason, new address or callback time; done when a cancelled test order shows the reason in its Shopify note
- [ ] 5.3 Make sure HaanJi never cancels or edits the order; done when a cancelled-on-call test order is still open in Shopify
- [ ] 5.4 Add the result sheet download for uploaded orders; done when downloading after calls gives every original column plus the result columns

## 6. Final check

- [ ] 6.1 Run 100 test orders end to end on the development store (mix of answers, no-answers and callbacks); done when every order ends with the right tag and no customer was called outside 9 AM–9 PM
- [ ] 6.2 Go live with one pilot brand for one week; done when their orders are being called and tagged with no manual help
