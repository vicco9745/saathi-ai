from fastapi import Header, HTTPException
from .db import get_key_record, log_usage

async def require_api_key(
    x_api_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    key = x_api_key
    if not key and authorization and authorization.lower().startswith("bearer "):
        key = authorization[7:].strip()

    if not key:
        raise HTTPException(401, "API key required")

    row = get_key_record(key)
    if not row or not row[4]:
        raise HTTPException(401, "Invalid or inactive API key")

    return row

def record_usage(row, service):
    log_usage(row[0], service)
