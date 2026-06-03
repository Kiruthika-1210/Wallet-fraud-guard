# ============================================================
# WALLET GUARD - FASTAPI APPLICATION
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ============================================================
# IMPORT ROUTERS
# ============================================================

from api.routers.wallet import (
    router as wallet_router
)


from api.routers.auth import (
     router as auth_router
)

from api.routers.fraud import (
     router as fraud_router
)

# ============================================================
# IMPORT SERVICES
# ============================================================

from api.services.fraud_model import (
    initialize_artifacts
)

from api.services.shap_explainer import (
    initialize_explainer
)

from api.services.audit_service import (
    initialize_audit_table
)

from api.services.db_service import (
    initialize_database
)

# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(

    title="Wallet Guard API",

    description=(
        "AI-Powered Hybrid Fraud "
        "Detection Platform"
    ),

    version="1.0.0"
)

# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

@app.on_event("startup")

def startup_event():

    print("\nInitializing Wallet Guard...")

    # --------------------------------------------------------
    # Initialize Database
    # --------------------------------------------------------

    initialize_database()

    # --------------------------------------------------------
    # Load ML Artifacts
    # --------------------------------------------------------

    initialize_artifacts()

    # --------------------------------------------------------
    # Initialize SHAP Explainer
    # --------------------------------------------------------

    initialize_explainer()

    # --------------------------------------------------------
    # Initialize Audit Tables
    # --------------------------------------------------------

    initialize_audit_table()

    print("\nWallet Guard Ready")

# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")

def health_check():

    return {

        "status": "running",

        "service": "Wallet Guard API",

        "version": "1.0.0"
    }

# ============================================================
# REGISTER ROUTERS
# ============================================================

app.include_router(

    wallet_router,

    prefix="/wallet",

    tags=["Wallet"]
)


app.include_router(
     auth_router,
     prefix="/auth",
     tags=["Authentication"]
)

app.include_router(
     fraud_router,
     prefix="/fraud",
     tags=["Fraud Monitoring"]
)

# ============================================================
# MAIN ENTRY
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "api.app:app",

        host="0.0.0.0",

        port=8000,

        reload=True
    )

