# ============================================================
# WALLET GUARD - AUDIT SERVICE
# ============================================================

import os
import json
import sqlite3
from datetime import datetime

# ============================================================
# DATABASE PATH
# ============================================================

DB_PATH = "db/wallet_fraud.db"

# ============================================================
# AUDIT LOG DIRECTORY
# ============================================================

AUDIT_LOG_DIR = "artifacts"

os.makedirs(
    AUDIT_LOG_DIR,
    exist_ok=True
)

# ============================================================
# CREATE FRAUD LOG TABLE
# ============================================================

def initialize_audit_table():

    connection = sqlite3.connect(
        DB_PATH
    )

    cursor = connection.cursor()

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

    print("\nFraud Audit Table Ready")

# ============================================================
# SAVE FRAUD LOG TO DATABASE
# ============================================================

def save_fraud_log(
    transaction_id,
    user_id,
    payload
):

    connection = sqlite3.connect(
        DB_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""

        INSERT INTO fraud_logs (

            transaction_id,
            user_id,
            decision,
            ml_risk_score,
            rule_risk_score,
            final_risk_score,
            triggered_rules,
            top_risk_factors,
            human_explanations,
            created_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        transaction_id,

        user_id,

        payload.get(
            "decision"
        ),

        payload.get(
            "ml_risk_score"
        ),

        payload.get(
            "rule_risk_score"
        ),

        payload.get(
            "final_risk_score"
        ),

        json.dumps(
            payload.get(
                "triggered_rules",
                []
            )
        ),

        json.dumps(
            payload.get(
                "top_risk_factors",
                []
            )
        ),

        json.dumps(
            payload.get(
                "human_explanations",
                []
            )
        ),

        datetime.utcnow().isoformat()
    ))

    connection.commit()

    connection.close()

    print(
        f"\nFraud Audit Log Saved "
        f"for Transaction: {transaction_id}"
    )

# ============================================================
# SAVE LOCAL JSON AUDIT FILE
# ============================================================

def save_local_audit_file(
    transaction_id,
    payload
):

    audit_file_path = os.path.join(

        AUDIT_LOG_DIR,

        f"{transaction_id}_audit.json"
    )

    with open(
        audit_file_path,
        "w"
    ) as file:

        json.dump(
            payload,
            file,
            indent=4
        )

    print(
        f"\nLocal Audit File Saved: "
        f"{audit_file_path}"
    )

# ============================================================
# FETCH ALL FRAUD LOGS
# ============================================================

def get_all_fraud_logs():

    connection = sqlite3.connect(
        DB_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""

        SELECT *

        FROM fraud_logs

        ORDER BY created_at DESC

    """)

    rows = cursor.fetchall()

    connection.close()

    return rows

# ============================================================
# FETCH USER FRAUD LOGS
# ============================================================

def get_user_fraud_logs(
    user_id
):

    connection = sqlite3.connect(
        DB_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""

        SELECT *

        FROM fraud_logs

        WHERE user_id = ?

        ORDER BY created_at DESC

    """, (user_id,))

    rows = cursor.fetchall()

    connection.close()

    return rows

# ============================================================
# FETCH SINGLE TRANSACTION LOG
# ============================================================

def get_transaction_log(
    transaction_id
):

    connection = sqlite3.connect(
        DB_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""

        SELECT *

        FROM fraud_logs

        WHERE transaction_id = ?

    """, (transaction_id,))

    row = cursor.fetchone()

    connection.close()

    return row

# ============================================================
# GENERATE AUDIT PAYLOAD
# ============================================================

def generate_audit_payload(
    transaction_id,
    user_id,
    payload
):

    return {

        "transaction_id": transaction_id,

        "user_id": user_id,

        "decision": payload.get(
            "decision"
        ),

        "ml_risk_score": payload.get(
            "ml_risk_score"
        ),

        "rule_risk_score": payload.get(
            "rule_risk_score"
        ),

        "final_risk_score": payload.get(
            "final_risk_score"
        ),

        "triggered_rules": payload.get(
            "triggered_rules",
            []
        ),

        "top_risk_factors": payload.get(
            "top_risk_factors",
            []
        ),

        "human_explanations": payload.get(
            "human_explanations",
            []
        ),

        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================
# COMPLETE AUDIT PIPELINE
# ============================================================

def process_audit_log(
    transaction_id,
    user_id,
    payload
):

    # --------------------------------------------------------
    # Generate Audit Payload
    # --------------------------------------------------------

    audit_payload = (
        generate_audit_payload(
            transaction_id,
            user_id,
            payload
        )
    )

    # --------------------------------------------------------
    # Save to Database
    # --------------------------------------------------------

    save_fraud_log(
        transaction_id,
        user_id,
        audit_payload
    )

    # --------------------------------------------------------
    # Save Local Audit File
    # --------------------------------------------------------

    save_local_audit_file(
        transaction_id,
        audit_payload
    )

    return audit_payload
