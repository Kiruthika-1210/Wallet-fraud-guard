# ============================================================
# WALLET GUARD - ANALYTICS SERVICE
# ============================================================

import sqlite3

DB_PATH = "db/wallet_fraud.db"

# ============================================================
# GET DATABASE CONNECTION
# ============================================================

def get_connection():

    return sqlite3.connect(DB_PATH)

# ============================================================
# FRAUD ANALYTICS
# ============================================================

def get_fraud_analytics():

    connection = get_connection()

    cursor = connection.cursor()

    # --------------------------------------------------------
    # TOTAL TRANSACTIONS
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        """
    )

    total_transactions = cursor.fetchone()[0]

    # --------------------------------------------------------
    # APPROVED
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE decision='APPROVE'
        """
    )

    approved_transactions = cursor.fetchone()[0]

    # --------------------------------------------------------
    # REVIEW
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE decision='REVIEW'
        """
    )

    review_transactions = cursor.fetchone()[0]

    # --------------------------------------------------------
    # REJECTED
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE decision='REJECT'
        """
    )

    rejected_transactions = cursor.fetchone()[0]

    connection.close()

    fraud_rate = 0

    if total_transactions > 0:

        fraud_rate = round(

            (rejected_transactions /
             total_transactions) * 100,

            2
        )

    return {

        "total_transactions":
            total_transactions,

        "approved_transactions":
            approved_transactions,

        "review_transactions":
            review_transactions,

        "rejected_transactions":
            rejected_transactions,

        "fraud_rate":
            fraud_rate
    }