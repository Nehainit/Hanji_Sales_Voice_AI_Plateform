-- HaanJi database schema (Postgres / Supabase).
-- Money is stored as integer paise (₹1 = 100 paise) to avoid rounding errors.

create table sellers (
  id          uuid primary key default gen_random_uuid(),
  brand_name  text not null,
  phone       text,
  email       text,
  language    text not null default 'hinglish',   -- hinglish | hindi | english
  voice       text not null default 'ananya',
  created_at  timestamptz not null default now()
);

create table stores (
  id            uuid primary key default gen_random_uuid(),
  seller_id     uuid not null references sellers(id) on delete cascade,
  platform      text not null,                    -- shopify | sheet
  shop_domain   text,                             -- e.g. kesarkurtis.myshopify.com
  access_token  text,                             -- encrypt before storing
  connected_at  timestamptz not null default now()
);

create table call_settings (
  seller_id          uuid primary key references sellers(id) on delete cascade,
  delay_minutes      int  not null default 5,
  window_start       time not null default '09:00',
  window_end         time not null default '21:00',
  max_attempts       int  not null default 3,
  retry_gap_minutes  int  not null default 120,
  rto_cost_paise     int  not null default 16000   -- ₹160, used for "money saved"
);

create table scripts (
  id          uuid primary key default gen_random_uuid(),
  seller_id   uuid not null references sellers(id) on delete cascade,
  template    text not null default 'cod_confirmation',
  lines       jsonb not null,                     -- same keys as flow_cod.SCRIPT
  updated_at  timestamptz not null default now()
);

create table orders (
  id                 uuid primary key default gen_random_uuid(),
  store_id           uuid not null references stores(id) on delete cascade,
  external_order_id  text not null,               -- Shopify order id / sheet row id
  customer_name      text not null,
  customer_phone     text not null,
  amount_paise       int  not null,
  product_summary    text,
  address            text,
  status             text not null default 'pending',  -- pending | confirmed | cancelled | callback | no_answer
  created_at         timestamptz not null default now(),
  unique (store_id, external_order_id)
);

create table calls (
  id                uuid primary key default gen_random_uuid(),
  order_id          uuid not null references orders(id) on delete cascade,
  attempt_no        int  not null,
  scheduled_at      timestamptz not null,
  started_at        timestamptz,
  ended_at          timestamptz,
  duration_seconds  int,
  status            text,                         -- answered | busy | not_answered | failed
  error             text,                         -- why a call failed, if it did
  outcome           text,                         -- confirmed | cancelled | callback | no_answer
  cancel_reason     text,
  new_address       text,
  callback_at       timestamptz,
  recording_url     text,
  transcript        jsonb,                        -- [{"role": "bot"|"customer", "text": "..."}]
  provider_call_id  text,                         -- Exotel call SID
  cost_paise        int
);

create table wallet_transactions (
  id            uuid primary key default gen_random_uuid(),
  seller_id     uuid not null references sellers(id) on delete cascade,
  amount_paise  int  not null,                    -- + recharge/credit, - call charge
  kind          text not null,                    -- recharge | call_charge | credit
  reference     text,                             -- Razorpay payment id or call id
  created_at    timestamptz not null default now()
);

create index on orders (store_id, status);
create index on calls (order_id);
create index on calls (scheduled_at) where started_at is null;
create index on wallet_transactions (seller_id, created_at);

-- Supabase exposes public tables through its API. With row level security on and no
-- policies, only the backend (service role key) can read or write. Per-seller policies
-- for the dashboard come in Phase 3 (add-seller-dashboard task 1.4).
alter table sellers             enable row level security;
alter table stores              enable row level security;
alter table call_settings       enable row level security;
alter table scripts             enable row level security;
alter table orders              enable row level security;
alter table calls               enable row level security;
alter table wallet_transactions enable row level security;
