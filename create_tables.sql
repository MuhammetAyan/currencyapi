CREATE TABLE IF NOT EXISTS public.currency (
    id serial PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    currency_code VARCHAR ( 10 ) NOT NULL,
    rate NUMERIC(10, 4) NOT NULL
);
