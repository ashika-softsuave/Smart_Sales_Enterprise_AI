from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.intent_detector import detect_intent
from app.services.task_allocator import allocate_task
from app.services.onboarding_service import onboard_user
from app.core.security import get_current_user
from app.core.database import get_db

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    intent = detect_intent(request.message)

    # 🔹 DAILY TASK
    if intent == "GET_DAILY_TASK":
        task = allocate_task(current_user.id)
        return ChatResponse(
            reply="📋 Here is your task plan for today",
            data=task
        )

    # 🔹 MANAGER DASHBOARD
    if intent == "MANAGER_DASHBOARD":
        if current_user.role != "manager":
            return ChatResponse(
                reply="❌ You are not authorized to view manager dashboard"
            )

        return ChatResponse(
            reply="📊 Manager dashboard is ready",
            data={"download_url": "/manager/report"}
        )

    # 🔹 UNKNOWN
    return ChatResponse(
        reply="🤔 I didn’t understand that. Try asking about tasks, dashboard, or onboarding."
    )
