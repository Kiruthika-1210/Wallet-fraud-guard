CREATE TABLE users (

    id SERIAL PRIMARY KEY,

    email VARCHAR(255) UNIQUE NOT NULL,

    password_hash TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE wallets (

    id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(id),

    balance NUMERIC(12,2) DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (

    id SERIAL PRIMARY KEY,

    transaction_id UUID UNIQUE NOT NULL,

    wallet_id INTEGER REFERENCES wallets(id),

    user_id INTEGER REFERENCES users(id),

    amount NUMERIC(12,2),

    ml_risk_score FLOAT,

    rule_risk_score FLOAT,

    final_risk_score FLOAT,

    decision VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fraud_audit_logs (

    id SERIAL PRIMARY KEY,

    transaction_id UUID,

    decision VARCHAR(20),

    triggered_rules JSONB,

    risk_factors JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fraud_daily_stats (

    id SERIAL PRIMARY KEY,

    stat_date DATE UNIQUE,

    total_transactions INTEGER,

    approved_count INTEGER,

    review_count INTEGER,

    rejected_count INTEGER,

    fraud_rate FLOAT
);

CREATE TABLE user_risk_profiles (

    id SERIAL PRIMARY KEY,

    user_id INTEGER,

    avg_risk_score FLOAT,

    total_transactions INTEGER,

    rejected_transactions INTEGER,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);