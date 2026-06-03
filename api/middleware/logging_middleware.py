# ============================================================
# WALLET GUARD - LOGGING MIDDLEWARE
# ============================================================

import time
import json
from datetime import datetime

from starlette.middleware.base import (
    BaseHTTPMiddleware
)

# ============================================================
# LOGGING MIDDLEWARE
# ============================================================

class LoggingMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request,
        call_next
    ):

        # ----------------------------------------------------
        # Request Start Time
        # ----------------------------------------------------

        start_time = time.time()

        # ----------------------------------------------------
        # Process Request
        # ----------------------------------------------------

        response = await call_next(
            request
        )

        # ----------------------------------------------------
        # Calculate Latency
        # ----------------------------------------------------

        latency_ms = (
            time.time() - start_time
        ) * 1000

        # ----------------------------------------------------
        # Build Log Payload
        # ----------------------------------------------------

        log_payload = {

            "timestamp": (
                datetime.utcnow()
                .isoformat()
            ),

            "method": request.method,

            "path": request.url.path,

            "status_code": (
                response.status_code
            ),

            "latency_ms": round(
                latency_ms,
                2
            )
        }

        # ----------------------------------------------------
        # Console Log
        # ----------------------------------------------------

        print(
            json.dumps(
                log_payload,
                indent=4
            )
        )

        # ----------------------------------------------------
        # Attach Header
        # ----------------------------------------------------

        response.headers[
            "X-Process-Time"
        ] = str(
            round(latency_ms, 2)
        )

        return response

