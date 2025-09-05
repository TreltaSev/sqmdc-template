from datetime import datetime, timedelta, timezone

def now() -> int:
    """
    Returns the current time in POSIX timestamp (UTC)
    """
    return int(datetime.now(timezone.utc).timestamp())

def future(delta: timedelta):
    """
    Returns the future with a given delta
    """
    return int((datetime.now(timezone.utc) + delta).timestamp())