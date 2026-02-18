from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.connection import get_connection
from src.api.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginIn(BaseModel):
    role: str  # "client" | "support"
    id: int


@router.post("/login")
def login(payload: LoginIn):
    conn = get_connection()

    if payload.role == "client":
        sql = "SELECT id FROM client WHERE id = %s"
        with conn.cursor() as cur:
            cur.execute(sql, (payload.id,))
            row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=401, detail="Invalid client id")

        token = create_access_token({"role": "client", "user_id": payload.id})

        return {"access_token": token, "token_type": "bearer"}

    if payload.role == "support":
        sql = "SELECT id, position_team FROM support_team WHERE id = %s"
        with conn.cursor() as cur:
            cur.execute(sql, (payload.id,))
            row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=401, detail="Invalid support id")

        token = create_access_token(
            {
                "role": "support",
                "user_id": payload.id,
                "position_team": row["position_team"],  # type: ignore
            }
        )

        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=400, detail="Invalid role")
