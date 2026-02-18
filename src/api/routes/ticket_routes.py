from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from db.connection import get_connection
from src.api.deps import CurrentUser, get_current_user
from src.tickets.ticket_services import TicketServices
from fastapi import Query
from pydantic import BaseModel
from typing import Optional


router = APIRouter(prefix="/tickets", tags=["tickets"])
AllowedStatus = Literal["open", "in_progress", "resolved", "canceled"]


class StatusUpdateIn(BaseModel):
    status: AllowedStatus


OTHER_CATEGORY_ID = 101


class AssignIn(BaseModel):
    support_id: int


class TicketCreateIn(BaseModel):
    category_id: int
    subject: Optional[str] = None
    description: Optional[str] = None


@router.post("")
def create_ticket(body: TicketCreateIn, user: CurrentUser = Depends(get_current_user)):
    try:
        if user.role != "client":
            raise HTTPException(
                status_code=403, detail="Only client can create tickets"
            )

        if body.category_id == 101:
            if not (body.subject and body.subject.strip()) or not (
                body.description and body.description.strip()
            ):
                raise HTTPException(
                    status_code=422,
                    detail="For category 101, subject and descript are required",
                )

        conn = get_connection()
        services = TicketServices(conn)

        ticket_id = services.create_ticket(
            client_id=user.user_id,
            problem_category_id=body.category_id,
            subject=body.subject,
            description=body.description,
        )

        if not ticket_id:
            raise HTTPException(
                status_code=400, detail="No support available for this category"
            )

        return {"ticket_id": ticket_id}

    except Exception as e:
        print("🔥 ERRO NO POST /tickets:", e)
        raise


@router.get("/mine")
def my_tickets(
    status: str | None = Query(default=None),
    user: CurrentUser = Depends(get_current_user),
):
    conn = get_connection()
    services = TicketServices(conn)

    data = services.get_my_tickets(user.role, user.user_id, status)
    return data


@router.get("/problem-categories")
def list_problem_categories():
    conn = get_connection()
    services = TicketServices(conn)

    categories = services.get_problem_categories()
    return categories


@router.get("/board")
def tickets_board(
    status: str = Query("in_progress"),
    user: CurrentUser = Depends(get_current_user),
):
    if user.role != "support" or user.position_team not in ("senior", "engineer"):
        raise HTTPException(status_code=403, detail="Forbidden")

    allowed = {"open", "in_progress", "resolved", "canceled", "all"}
    if status not in allowed:
        raise HTTPException(status_code=422, detail="Invalid status")

    conn = get_connection()
    services = TicketServices(conn)
    return services.list_all_tickets_by_status(status)


@router.get("/board")
def board(
    status: str = Query("in_progress"),
    user: CurrentUser = Depends(get_current_user),
):
    if user.role != "support" or user.position_team not in ("senior", "engineer"):
        raise HTTPException(status_code=403, detail="Forbidden")

    allowed = {"open", "in_progress", "resolved", "canceled", "all"}
    if status not in allowed:
        raise HTTPException(status_code=422, detail="Invalid status")

    conn = get_connection()
    services = TicketServices(conn)
    return services.list_board_tickets(status)


@router.get("/{ticket_id}/available-supports")
def available_supports(
    ticket_id: int,
    user: CurrentUser = Depends(get_current_user),
):
    if user.role != "support" or user.position_team not in ("senior", "engineer"):
        raise HTTPException(status_code=403, detail="Forbidden")

    conn = get_connection()
    services = TicketServices(conn)

    data, err = services.list_available_supports_for_ticket(ticket_id)
    if err:
        raise HTTPException(status_code=400, detail=err)

    return data


@router.patch("/{ticket_id}/assign")
def assign_ticket(
    ticket_id: int,
    body: AssignIn,
    user: CurrentUser = Depends(get_current_user),
):
    if user.role != "support" or user.position_team not in ("senior", "engineer"):
        raise HTTPException(status_code=403, detail="Forbidden")

    conn = get_connection()
    services = TicketServices(conn)

    updated, err = services.reassign_ticket_and_return(
        ticket_id=ticket_id,
        new_support_id=body.support_id,
        actor_type=user.role,
        actor_id=user.user_id,
    )

    if err:
        raise HTTPException(status_code=400, detail=err)

    # retorna ticket atualizado
    if isinstance(updated, dict):
        return updated

    keys = [
        "ticket_id",
        "status",
        "create_date",
        "resolution_date",
        "client_id",
        "client_name",
        "category_id",
        "category_name",
        "required_level",
        "support_id",
        "support_name",
        "subject_user",
        "description_user",
    ]
    return dict(zip(keys, updated))  # type: ignore


@router.get("/{ticket_id}")
def ticket_details(ticket_id: int, user: CurrentUser = Depends(get_current_user)):
    conn = get_connection()
    services = TicketServices(conn)

    data = services.get_ticket_details(ticket_id)
    if not data:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # client só pode ver o próprio ticket
    if user.role == "client":
        client_id = data["client_id"] if isinstance(data, dict) else data[4]
        if client_id != user.user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

    return data


@router.patch("/{ticket_id}/status")
def update_status(
    ticket_id: int, body: StatusUpdateIn, user: CurrentUser = Depends(get_current_user)
):
    if user.role != "support":
        raise HTTPException(status_code=403, detail="Only support can change status")

    conn = get_connection()
    services = TicketServices(conn)

    details = services.get_ticket_details(ticket_id)
    if not details:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # junior/mid só mexe se ticket estiver atribuído a ele
    if user.position_team in ("junior", "mid_level"):
        owner_row = services.get_ticket_support_owner(ticket_id)
        if not owner_row:
            raise HTTPException(status_code=404, detail="Ticket not found")

        owner_id = (
            owner_row["id_support"] if isinstance(owner_row, dict) else owner_row[0]
        )
        if owner_id != user.user_id:
            raise HTTPException(
                status_code=403, detail="You can only update your assigned tickets"
            )

        updated = services.update_ticket_status_and_return(
            ticket_id=ticket_id,
            new_status=body.status,
            actor_type=user.role,
            actor_id=user.user_id,
        )

    if not updated:
        raise HTTPException(status_code=500, detail="Could not fetch updated ticket")

    if isinstance(updated, dict):
        return updated

    keys = [
        "ticket_id",
        "status",
        "create_date",
        "resolution_date",
        "client_id",
        "client_name",
        "category_id",
        "category_name",
        "required_level",
        "support_id",
        "support_name",
        "subject_user",
        "description_user",
    ]
    return dict(zip(keys, updated))


@router.get("/{ticket_id}/history")
def ticket_history(ticket_id: int, user: CurrentUser = Depends(get_current_user)):
    conn = get_connection()
    services = TicketServices(conn)

    # Reusa a mesma regra de permissão do details:
    details = services.get_ticket_details(ticket_id)
    if not details:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if user.role == "client":
        client_id = details["client_id"] if isinstance(details, dict) else details[4]
        if client_id != user.user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

    return services.get_ticket_history(ticket_id)


@router.get("/by-status")
def tickets_by_status(
    status: str | None = Query(default="in_progress"),
    user: CurrentUser = Depends(get_current_user),
):
    if user.role != "support" or user.position_team not in ("senior", "engineer"):
        raise HTTPException(status_code=403, detail="Forbidden")

    conn = get_connection()
    services = TicketServices(conn)
    return services.get_tickets_by_status(status)
