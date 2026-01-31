from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.intent_detector import detect_intent
from app.services.task_allocator import allocate_task_from_chat
from app.services.onboarding_service import onboard_user
from app.core.security import get_current_user
from app.core.database import get_db
from app.services.location_service import (
    set_waiting_for_location,
    set_user_location,
    get_user_location_context
)


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    intent = detect_intent(request.message)

    #SMALL TALK
    if intent == "SMALL_TALK":
        return ChatResponse(
            reply=(
                f"👋 Hi {current_user.name}! I’m your Sales AI Assistant.\n\n"
                "You can ask me:\n"
                "• What is my task today?\n"
                "• Show my dashboard\n"
                "• Manager dashboard\n"
                "• Download reports"
            )
        )

    #DAILY TASK
    if intent == "GET_DAILY_TASK":

        context = get_user_location_context(current_user.id)

        # Step 1: Ask for location
        if not context or context.get("awaiting_location") is False:
            set_waiting_for_location(current_user.id)
            return ChatResponse(
                reply="📍 Where are you right now? (Area or landmark)"
            )

    #TASK UPDATE (placeholder for DB logic)
    if intent == "UPDATE_TASK":
        return ChatResponse(
            reply="✅ Got it! I’ve marked this task as completed. Keep going 💪"
        )

    #ONBOARDING
    if intent == "ONBOARD_USER":
        result = onboard_user(request, db)
        return ChatResponse(
            reply="✅ User onboarded successfully.",
            data=result
        )

    #MANAGER DASHBOARD
    if intent == "MANAGER_DASHBOARD":
        if current_user.role != "manager":
            return ChatResponse(
                reply="❌ You are not authorized to view the manager dashboard."
            )

        return ChatResponse(
            reply="📊 Manager dashboard is ready.",
            data={
                "download_url": "/manager/report",
                "note": "Includes team performance and route efficiency."
            }
        )

    #SALESMAN DASHBOARD
    if intent == "SALESMAN_DASHBOARD":
        if current_user.role != "salesman":
            return ChatResponse(
                reply="❌ This dashboard is only for salesmen."
            )

        return ChatResponse(
            reply="📈 Your performance dashboard.",
            data={
                "tasks_completed": 2,
                "tasks_pending": 3
            }
        )

    #CEO DASHBOARD
    if intent == "CEO_DASHBOARD":
        if current_user.role != "ceo":
            return ChatResponse(
                reply="❌ Only the CEO can access this dashboard."
            )

        return ChatResponse(
            reply="🏢 CEO overview dashboard.",
            data={
                "total_sales": 125000,
                "top_region": "Chennai",
                "growth": "12%"
            }
        )
    #USER PROVIDES LOCATION
    context = get_user_location_context(current_user.id)

    if context and context.get("awaiting_location"):
        set_user_location(current_user.id, request.message)

        task = allocate_task_from_chat(
            current_user.id,
            request.message
        )

        return ChatResponse(
            reply="📋 Here’s your optimized task plan for today.",
            data=task
        )

    #FALLBACK
    return ChatResponse(
        reply=(
            "🤔 I’m not sure I understood that.\n\n"
            "Try asking:\n"
            "• What is my task today?\n"
            "• Show my dashboard\n"
            "• Manager dashboard"
        )
    )
