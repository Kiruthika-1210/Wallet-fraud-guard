# ============================================================
# WALLET GUARD - FRAUD ROUTER
# ============================================================

from fastapi import APIRouter
from fastapi import Depends
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

from api.dependencies import (
    get_current_user
)

from api.services.analytics_service import (
    get_fraud_analytics
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

def fetch_all_fraud_logs(current_user=Depends(get_current_user)):

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

def fetch_rejected_transactions(current_user=Depends(get_current_user)):

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
def analytics(
    current_user=Depends(get_current_user)
):

    return get_fraud_analytics()

