# ============================================================
# WALLET GUARD - WALLET ROUTER
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import uuid
import time

# ============================================================
# IMPORT SERVICES
# ============================================================

from api.services.feature_builder import (
    build_features
)

from api.services.fraud_model import (
    predict
)

from api.services.decision_engine import (
    generate_decision_payload
)

from api.services.shap_explainer import (
    analyze_transaction
)

from api.services.audit_service import (
    process_audit_log
)

from api.services.db_service import (
    save_transaction,
    get_wallet_balance,
    update_wallet_balance
)
# ============================================================
# ROUTER INITIALIZATION
# ============================================================

router = APIRouter()

# ============================================================
# REQUEST MODEL
# ============================================================

class TransactionRequest(BaseModel):

    user_id: int

    wallet_id: int

    amount: float

# ============================================================
# MOCK USER ANALYTICS
# ============================================================

# In production:
# these come from database analytics

import random

def get_user_transaction_stats(
    user_id
):

    avg_transaction = random.randint(
        1500,
        6000
    )

    std_transaction = random.randint(
        600,
        2500
    )

    last_10_min_txns = [

        random.randint(
            100,
            5000
        )

        for _ in range(
            random.randint(
                1,
                20
            )
        )
    ]

    return {

        "avg_transaction": avg_transaction,

        "std_transaction": std_transaction,

        "last_10_min_txns": last_10_min_txns
    }
# ============================================================
# WALLET TRANSFER ENDPOINT
# ============================================================

@router.post("/transfer")

def transfer_money(
    request: TransactionRequest
):
    start_time = time.perf_counter()
    # --------------------------------------------------------
    # Generate Transaction ID
    # --------------------------------------------------------

    transaction_id = (
        str(uuid.uuid4())
    )

    # --------------------------------------------------------
    # Fetch User Analytics
    # --------------------------------------------------------

    user_stats = (
        get_user_transaction_stats(
            request.user_id
        )
    )

    # --------------------------------------------------------
    # Build Features
    # --------------------------------------------------------

    features = build_features(

        txn_amount=request.amount,

        user_avg=user_stats[
            "avg_transaction"
        ],

        user_std=user_stats[
            "std_transaction"
        ],

        last_10_min_txns=user_stats[
            "last_10_min_txns"
        ],

        timestamp=datetime.utcnow()
    )

    # --------------------------------------------------------
    # ML Fraud Risk Score
    # --------------------------------------------------------

    ml_risk_score = predict(
        features
    )

    # --------------------------------------------------------
    # Hybrid Decision Engine
    # --------------------------------------------------------

    decision_payload = (
        generate_decision_payload(
            ml_risk_score,
            features
        )
    )

    # --------------------------------------------------------
    # SHAP Explainability
    # --------------------------------------------------------

    shap_payload = (
        analyze_transaction(
            features
        )
    )

    # --------------------------------------------------------
    # Merge Responses
    # --------------------------------------------------------

    final_payload = {

        "transaction_id": (
            transaction_id
        ),

        "wallet_id": (
            request.wallet_id
        ),

        "user_id": (
            request.user_id
        ),

        "amount": (
            request.amount
        ),

        **decision_payload,

        **shap_payload
    }

    # --------------------------------------------------------
    # Audit Logging
    # --------------------------------------------------------

    process_audit_log(

        transaction_id=transaction_id,

        user_id=request.user_id,

        payload=final_payload
    )

    save_transaction(
    transaction_id=transaction_id,
    user_id=request.user_id,
    wallet_id=request.wallet_id,
    amount=request.amount,
    decision=decision_payload["decision"],
    risk_score=decision_payload["final_risk_score"]
    )

    if decision_payload["decision"] == "APPROVE":

        current_balance = get_wallet_balance(
            request.wallet_id
        )

        if current_balance is not None:

            if current_balance >= request.amount:

                update_wallet_balance(

                    request.wallet_id,

                    current_balance - request.amount
                )

            else:

                return {

                    "success": False,

                    "message": "Insufficient wallet balance"
                }
    # --------------------------------------------------------
    # Final API Response
    # --------------------------------------------------------

    end_time = time.perf_counter()
    
    latency_ms = round(
        (end_time - start_time) * 1000,
        2
    )

    final_payload["latency_ms"] = latency_ms

    return {

        "success": True,

        "message": (
            "Transaction processed successfully"
        ),

        "data": final_payload
    }
