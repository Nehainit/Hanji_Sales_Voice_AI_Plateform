# Services checklist

Accounts to create, in the order you need them. Start the slow ones (KYC) first.
Check each provider's current requirements and pricing on their site.

## Do now (slow approvals)

- [ ] **Company registration** (Pvt Ltd or LLP). Exotel and Razorpay KYC ask for business documents.
- [ ] **Exotel**: sign up, complete KYC, buy an ExoPhone. Ask them which number type and
      TRAI rules apply to order-confirmation (transactional) calls, and how to enable the
      Voicebot / audio streaming applet.

## Phase 1: first real call

- [ ] **Sarvam AI**: API key (speech-to-text + text-to-speech for Hindi/Hinglish)
- [ ] **Anthropic**: API key from console.anthropic.com
- [ ] **ngrok** (free): lets Exotel reach the backend running on your laptop while testing

## Phase 2: real orders

- [ ] **Shopify Partner account** (free). Start with a custom app per pilot store;
      a public App Store listing needs Shopify review later.
- [ ] **Supabase** project (free tier): run `database/schema.sql` in its SQL editor
- [ ] **Redis**: local install for testing; a managed Redis when hosted
- [ ] **AWS account**: Mumbai region (ap-south-1)

## Phase 4: payments

- [ ] **Razorpay**: KYC, then API keys

## Legal basics before the first pilot

- [ ] Privacy policy and terms of service
- [ ] Recording disclosure line at the start of every call
- [ ] Data handling in line with India's DPDP Act 2023
