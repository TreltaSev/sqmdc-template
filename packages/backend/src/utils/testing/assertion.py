# === Utils ===
from utils.console import console

# === Typing ===
from httpx import Response
from fastapi import status

def assert_response_ok(response: Response):
    """
    Testing helper method to check if the response has a 200 status code
    """
    try:
        assert response.status_code == status.HTTP_200_OK
    except AssertionError:
        console.error(f"==== FAILED DUMP ====")
        console.error(f"Content: {response.content}")
        raise
    
def assert_response(response: Response, code: int):
    """
    Testing helper method to check if the response has a {x} status code
    """
    
    try:
        assert response.status_code == code
    except AssertionError:
        console.error(f"==== FAILED DUMP ====")
        console.error(f"Content: {response.content}")
        raise