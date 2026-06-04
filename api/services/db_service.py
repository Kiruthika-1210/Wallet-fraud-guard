# ============================================================
# WALLET GUARD - DATABASE SERVICE
# ============================================================

import sqlite3
from datetime import datetime

# ============================================================
# DATABASE PATH
# ============================================================

DB_PATH = "db/wallet_fraud.db"

# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return sqlite3.connect(
        DB_PATH
    )

# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    # --------------------------------------------------------
    # USERS TABLE
    # --------------------------------------------------------

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            email TEXT UNIQUE,

            password_hash TEXT,

            created_at TEXT
        )

    """)

    # --------------------------------------------------------
    # WALLETS TABLE
    # --------------------------------------------------------

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS wallets (

            wallet_id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            balance REAL DEFAULT 0,

            status TEXT DEFAULT 'ACTIVE',

            created_at TEXT
        )

    """)

    # --------------------------------------------------------
    # TRANSACTIONS TABLE
    # --------------------------------------------------------

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS transactions (

            transaction_id TEXT PRIMARY KEY,

            user_id INTEGER,

            wallet_id INTEGER,

            amount REAL,

            decision TEXT,

            risk_score REAL,

            created_at TEXT
        )

    """)

    # --------------------------------------------------------
    # FRAUD LOGS TABLE
    # --------------------------------------------------------

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS fraud_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            transaction_id TEXT,

            user_id INTEGER,

            decision TEXT,

            ml_risk_score REAL,

            rule_risk_score REAL,

            final_risk_score REAL,

            triggered_rules TEXT,

            top_risk_factors TEXT,

            human_explanations TEXT,

            created_at TEXT
        )

    """)

    connection.commit()

    connection.close()

    print("\nDatabase Initialized Successfully")

# ============================================================
# CREATE USER
# ============================================================

def create_user(
    name,
    email,
    password_hash
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        INSERT INTO users (

            name,
            email,
            password_hash,
            created_at

        )

        VALUES (?, ?, ?, ?)

    """, (

        name,

        email,

        password_hash,

        datetime.utcnow().isoformat()
    ))

    user_id = cursor.lastrowid
    
    connection.commit()
    
    connection.close()
    
    return user_id

# ============================================================
# CREATE WALLET
# ============================================================

def create_wallet(
    user_id,
    initial_balance=10000
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        INSERT INTO wallets (

            user_id,
            balance,
            created_at

        )

        VALUES (?, ?, ?)

    """, (

        user_id,

        initial_balance,

        datetime.utcnow().isoformat()
    ))

    connection.commit()

    connection.close()

# ============================================================
# GET WALLET BALANCE
# ============================================================

def get_wallet_balance(
    wallet_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        SELECT balance

        FROM wallets

        WHERE wallet_id = ?

    """, (wallet_id,))

    result = cursor.fetchone()

    connection.close()

    if result:

        return result[0]

    return None

# ============================================================
# UPDATE WALLET BALANCE
# ============================================================

def update_wallet_balance(
    wallet_id,
    new_balance
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        UPDATE wallets

        SET balance = ?

        WHERE wallet_id = ?

    """, (

        new_balance,

        wallet_id
    ))

    connection.commit()

    connection.close()

# ============================================================
# SAVE TRANSACTION
# ============================================================

def save_transaction(
    transaction_id,
    user_id,
    wallet_id,
    amount,
    decision,
    risk_score
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        INSERT INTO transactions (

            transaction_id,
            user_id,
            wallet_id,
            amount,
            decision,
            risk_score,
            created_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        transaction_id,

        user_id,

        wallet_id,

        amount,

        decision,

        risk_score,

        datetime.utcnow().isoformat()
    ))

    connection.commit()

    connection.close()

# ============================================================
# FETCH USER TRANSACTIONS
# ============================================================

def get_user_transactions(
    user_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        SELECT *

        FROM transactions

        WHERE user_id = ?

        ORDER BY created_at DESC

    """, (user_id,))

    rows = cursor.fetchall()

    connection.close()

    return rows

# ============================================================
# FETCH FRAUD TRANSACTIONS
# ============================================================

def get_fraud_transactions():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        SELECT *

        FROM transactions

        WHERE decision = 'REJECT'

        ORDER BY created_at DESC

    """)

    rows = cursor.fetchall()

    connection.close()

    return rows

# ============================================================
# CHECK WALLET EXISTS
# ============================================================

def wallet_exists(
    wallet_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        SELECT wallet_id

        FROM wallets

        WHERE wallet_id = ?

    """, (wallet_id,))

    result = cursor.fetchone()

    connection.close()

    return result is not None

