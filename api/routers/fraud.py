# ============================================================
# WALLET GUARD - FRAUD ROUTER
# ============================================================

from fastapi import APIRouter

# ============================================================
# IMPORT SERVICES
# ============================================================

from api.services.audit_service import (

    get_all_fraud_logs,

    get_user_fraud_logs,

    get_transaction_log
)

from api.services.db_service import (

    get_fraud_transactions
)

# ============================================================
# ROUTER INITIALIZATION
# ============================================================

router = APIRouter()

# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/health")

def fraud_health_check():

    return {

        "status": "running",

        "service": "Fraud Monitoring API"
    }

# ============================================================
# GET ALL FRAUD LOGS
# ============================================================

@router.get("/logs")

def fetch_all_fraud_logs():

    logs = get_all_fraud_logs()

    return {

        "success": True,

        "total_logs": len(logs),

        "data": logs
    }

# ============================================================
# GET USER FRAUD LOGS
# ============================================================

@router.get("/logs/user/{user_id}")

def fetch_user_fraud_logs(
    user_id: int
):

    logs = get_user_fraud_logs(
        user_id
    )

    return {

        "success": True,

        "user_id": user_id,

        "total_logs": len(logs),

        "data": logs
    }

# ============================================================
# GET SINGLE TRANSACTION LOG
# ============================================================

@router.get("/transaction/{transaction_id}")

def fetch_transaction_log(
    transaction_id: str
):

    transaction_log = (
        get_transaction_log(
            transaction_id
        )
    )

    if not transaction_log:

        return {

            "success": False,

            "message": (
                "Transaction log not found"
            )
        }

    return {

        "success": True,

        "data": transaction_log
    }

# ============================================================
# GET REJECTED FRAUD TRANSACTIONS
# ============================================================

@router.get("/rejected")

def fetch_rejected_transactions():

    transactions = (
        get_fraud_transactions()
    )

    return {

        "success": True,

        "total_rejected": (
            len(transactions)
        ),

        "data": transactions
    }

# ============================================================
# FRAUD ANALYTICS SUMMARY
# ============================================================

@router.get("/analytics")

def fraud_analytics():

    logs = get_all_fraud_logs()

    total_transactions = len(logs)

    rejected = 0

    review = 0

    approved = 0

    for log in logs:

        decision = log[3]

        if decision == "REJECT":

            rejected += 1

        elif decision == "REVIEW":

            review += 1

        else:

            approved += 1

    fraud_rate = 0

    if total_transactions > 0:

        fraud_rate = (
            rejected / total_transactions
        ) * 100

    return {

        "success": True,

        "analytics": {

            "total_transactions": (
                total_transactions
            ),

            "approved_transactions": (
                approved
            ),

            "review_transactions": (
                review
            ),

            "rejected_transactions": (
                rejected
            ),

            "fraud_rate_percentage": round(
                fraud_rate,
                2
            )
        }
    }

