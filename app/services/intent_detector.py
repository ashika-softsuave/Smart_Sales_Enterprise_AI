# app/services/intent_detector.py

def detect_intent(message: str) -> str:
    msg = message.lower()

    # 🔹 Small talk
    if any(greet in msg for greet in ["hi", "hello", "hey", "good morning", "good evening"]):
        return "SMALL_TALK"

    #  Daily task allocation
    if any(word in msg for word in ["today task", "today's task", "my task", "route", "where should i go"]):
        return "GET_DAILY_TASK"

    # 🔹 Task update / completion
    if any(word in msg for word in ["completed", "finished", "done", "visited"]):
        return "UPDATE_TASK"

    # 🔹 Onboarding
    if any(word in msg for word in ["register", "onboard", "new user"]):
        return "ONBOARD_USER"

    # 🔹 Dashboards
    if "dashboard" in msg and "manager" in msg:
        return "MANAGER_DASHBOARD"

    if "dashboard" in msg and "ceo" in msg:
        return "CEO_DASHBOARD"

    if "dashboard" in msg:
        return "SALESMAN_DASHBOARD"

    # 🔹 Download
    if "download" in msg or "export" in msg:
        return "DOWNLOAD_REPORT"

    return "UNKNOWN"
