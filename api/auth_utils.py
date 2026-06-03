# ============================================================
# WALLET GUARD - AUTH UTILITIES
# ============================================================

from datetime import (
    datetime,
    timedelta
)

from jose import jwt

# ============================================================
# JWT CONFIGURATION
# ============================================================

SECRET_KEY = (
    "wallet_guard_secret_key"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ============================================================
# CREATE ACCESS TOKEN
# ============================================================

def create_access_token(
    data: dict
):

    to_encode = data.copy()

    expire = (
        datetime.utcnow()
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update({

        "exp": expire
    })

    encoded_jwt = jwt.encode(

        to_encode,

        SECRET_KEY,

        algorithm=ALGORITHM
    )

    return encoded_jwt

# ============================================================
# VERIFY ACCESS TOKEN
# ============================================================

def verify_access_token(
    token: str
):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )

        return payload

    except Exception:

        return None

