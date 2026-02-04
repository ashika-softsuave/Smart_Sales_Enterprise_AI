def detect_intent(message: str) -> str:
    msg = message.lower()

    # 🔹 END OF DAY / SUMMARY (HIGHEST PRIORITY)
    if any(phrase in msg for phrase in [
        "done for this day",
        "done with my day",
        "done for today",
        "done for the day",
        "i am done",
        "finished my day",
        "end of day",
        "end my day",
        "closing my day",
        "will continue tomorrow",
        "continue next day",
        "pending"
    ]):
        return "END_OF_DAY_REPORT"

    # 🔹 DAILY TASK
    if "task" in msg and ("today" in msg or "now" in msg):
        return "GET_DAILY_TASK"

    # 🔹 TASK PROGRESS UPDATE
    if any(word in msg for word in [
        "completed", "visited", "sold"
    ]):
        return "UPDATE_TASK"

    # 🔹 MANAGER PERFORMANCE / SALES TRACKING  ✅ NEW
    if any(phrase in msg for phrase in [
        "track sales",
        "sales performance",
        "team performance",
        "team sales",
        "sales report",
        "performance report",
        "leaderboard"
    ]):
        return "MANAGER_SALES_OVERVIEW"

    # 🔹 SMALL TALK
    if any(greet in msg for greet in [
        "hi", "hello", "hey", "good morning", "good evening"
    ]):
        return "SMALL_TALK"

    # 🔹 ONBOARDING
    if any(word in msg for word in [
        "register", "onboard", "new user"
    ]):
        return "ONBOARD_USER"

    # 🔹 DASHBOARDS (explicit)
    if "dashboard" in msg and "manager" in msg:
        return "MANAGER_DASHBOARD"

    if "dashboard" in msg and "ceo" in msg:
        return "CEO_DASHBOARD"

    if "dashboard" in msg:
        return "SALESMAN_DASHBOARD"

    return "UNKNOWN"
