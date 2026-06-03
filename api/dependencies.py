# ============================================================
# WALLET GUARD - JWT DEPENDENCIES
# ============================================================

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from api.auth_utils import (
    verify_access_token
)

# ============================================================
# JWT SECURITY SCHEME
# ============================================================

security = HTTPBearer()

# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user(

    credentials: HTTPAuthorizationCredentials = Depends(
        security
    )
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid or expired token"
        )

    return payload