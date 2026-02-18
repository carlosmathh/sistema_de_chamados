from fastapi import HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from src.api.security import decode_token

bearer_scheme = HTTPBearer(auto_error=True)


class CurrentUser(BaseModel):
    role: str
    user_id: int
    position_team: str | None = None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> CurrentUser:
    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return CurrentUser(**payload)


# Guards de permissão
def require_roles(*allowed_roles: str):
    def _guard(user: CurrentUser = Security(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return _guard


def require_support_positions(*allowed_positions: str):
    def _guard(user: CurrentUser = Security(get_current_user)):
        if user.role != "support":
            raise HTTPException(status_code=403, detail="Forbidden")

        if user.position_team not in allowed_positions:
            raise HTTPException(status_code=403, detail="Forbidden")

        return user

    return _guard
