# === Utils
from utils.globals import session

# === Typing ===
from fastapi import Cookie, HTTPException, status
from typing import Annotated


def require_session(session_token: Annotated[str | None, Cookie()] = None) -> str:
    """
    When used as a dependency, the user must submit a valid session_token through the cookies header.
    If the session_token isn't valid, return 401, other wise, call the next decorated function

    :param str | None session_token: session_token in cookie header
    """

    if session_token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "No session_token given")

    if session_token not in session:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Session token is invalid")

    return session_token
