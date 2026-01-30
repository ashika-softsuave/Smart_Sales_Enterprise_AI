def detect_intent(message: str) -> str:
    msg = message.lower()

    if "task" in msg or "today" in msg or "route" in msg:
        return "GET_DAILY_TASK"

    if "register" in msg or "onboard" in msg or "new" in msg:
        return "ONBOARD_USER"

    if "dashboard" in msg and "manager" in msg:
        return "MANAGER_DASHBOARD"

    if "dashboard" in msg:
        return "SALESMAN_DASHBOARD"

    if "download" in msg:
        return "DOWNLOAD_REPORT"

    return "UNKNOWN"
