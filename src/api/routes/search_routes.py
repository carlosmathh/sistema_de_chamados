from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Literal

from db.connection import get_connection
from src.api.deps import CurrentUser, get_current_user
from search.search_services import SearchServices

router = APIRouter(prefix="/tickets", tags=["tickets"])

AllowedStatus = Literal["open", "in_progress", "resolved", "canceled"]


def can_use_search(user: CurrentUser) -> bool:
    # client pode buscar (sempre "meus tickets")
    if user.role == "client":
        return True

    # support só senior/engineer (igual seu menu)
    if user.role == "support" and user.position_team in ("senior", "engineer"):
        return True

    return False


@router.get("/search")
def search_tickets(
    mode: Literal["id", "text"] = Query(..., description="id | text"),
    ticket_id: int | None = Query(None, ge=1, description="Obrigatório quando mode=id"),
    q: str | None = Query(
        None, min_length=1, description="Obrigatório quando mode=text"
    ),
    status: AllowedStatus | None = Query(None, description="Filtro opcional"),
    user: CurrentUser = Depends(get_current_user),
):
    # Permissão
    if not can_use_search(user):
        raise HTTPException(status_code=403, detail="You are not allowed to use search")

    conn = get_connection()
    services = SearchServices(conn)

    client_id = user.user_id if user.role == "client" else None

    if mode == "id":
        if ticket_id is None:
            raise HTTPException(
                status_code=422, detail="ticket_id is required when mode=id"
            )

        result = services.search_ticket_by_id(
            user_role=user.role,
            ticket_id=ticket_id,
            client_id=client_id,
            status=status,
        )

        if not result:
            return []

        return [result]

    # mode == "text"
    if q is None or not q.strip():
        raise HTTPException(status_code=422, detail="q is required when mode=text")

    results = services.search_tickets_by_text(
        user_role=user.role,
        text=q,
        client_id=client_id,
        status=status,
    )

    return results or []
