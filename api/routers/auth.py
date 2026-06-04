# ============================================================
# WALLET GUARD - AUTH ROUTER
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from passlib.context import CryptContext
import sqlite3
from datetime import datetime

# ============================================================
# IMPORT AUTH UTILITIES
# ============================================================

from api.auth_utils import (
    create_access_token
)

from api.services.db_service import (
    create_wallet
)

# ============================================================
# DATABASE PATH
# ============================================================

DB_PATH = "db/wallet_fraud.db"

# ============================================================
# PASSWORD HASHING
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ============================================================
# ROUTER INITIALIZATION
# ============================================================

router = APIRouter()

# ============================================================
# REQUEST MODELS
# ============================================================

class RegisterRequest(BaseModel):

    name: str

    email: str

    password: str

class LoginRequest(BaseModel):

    email: str

    password: str

# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return sqlite3.connect(
        DB_PATH
    )

# ============================================================
# HASH PASSWORD
# ============================================================

def hash_password(
    password
):

    return pwd_context.hash(
        password
    )

# ============================================================
# VERIFY PASSWORD
# ============================================================

def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# ============================================================
# REGISTER USER
# ============================================================

@router.post("/register")

def register(
    request: RegisterRequest
):

    connection = get_connection()

    cursor = connection.cursor()

    # --------------------------------------------------------
    # Check Existing User
    # --------------------------------------------------------

    cursor.execute("""

        SELECT id

        FROM users

        WHERE email = ?

    """, (request.email,))

    existing_user = cursor.fetchone()

    if existing_user:

        connection.close()

        return {

            "success": False,

            "message": (
                "User already exists"
            )
        }

    # --------------------------------------------------------
    # Hash Password
    # --------------------------------------------------------

    password_hash = hash_password(
        request.password
    )

    # --------------------------------------------------------
    # Insert User
    # --------------------------------------------------------

    cursor.execute("""

        INSERT INTO users (

            name,
            email,
            password_hash,
            created_at

        )

        VALUES (?, ?, ?, ?)

    """, (

        request.name,

        request.email,

        password_hash,

        datetime.utcnow().isoformat()
    ))

    user_id = cursor.lastrowid

    connection.commit()

    connection.close()

    create_wallet(
    user_id=user_id,
    initial_balance=10000
    )

    return {

        "success": True,

        "message": (
            "User registered successfully"
        )
    }

# ============================================================
# LOGIN USER
# ============================================================

@router.post("/login")

def login(
    request: LoginRequest
):

    connection = get_connection()

    cursor = connection.cursor()

    # --------------------------------------------------------
    # Fetch User
    # --------------------------------------------------------

    cursor.execute("""

        SELECT id,
               name,
               email,
               password_hash

        FROM users

        WHERE email = ?

    """, (request.email,))

    user = cursor.fetchone()

    connection.close()

    # --------------------------------------------------------
    # User Validation
    # --------------------------------------------------------

    if not user:

        return {

            "success": False,

            "message": (
                "Invalid credentials"
            )
        }

    user_id = user[0]

    user_name = user[1]

    user_email = user[2]

    stored_password_hash = user[3]

    # --------------------------------------------------------
    # Password Verification
    # --------------------------------------------------------

    valid_password = verify_password(

        request.password,

        stored_password_hash
    )

    if not valid_password:

        return {

            "success": False,

            "message": (
                "Invalid credentials"
            )
        }

    # --------------------------------------------------------
    # Generate JWT Token
    # --------------------------------------------------------

    token = create_access_token({

        "user_id": user_id,

        "email": user_email
    })

    return {

        "success": True,

        "message": (
            "Login successful"
        ),

        "access_token": token,

        "user": {

            "id": user_id,

            "name": user_name,

            "email": user_email
        }
    }

# ============================================================
# AUTH HEALTH CHECK
# ============================================================

@router.get("/health")

def auth_health_check():

    return {

        "status": "running",

        "service": "Authentication API"
    }

