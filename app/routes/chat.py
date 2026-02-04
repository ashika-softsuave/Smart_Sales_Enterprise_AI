from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date

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
from app.services.message_parser import extract_pending_items
from app.services.sales_target_service import get_salesman_daily_target
from app.models.daily_sales_log import DailySalesLog

# DEFINE ROUTER
router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # HANDLE LOCATION RESPONSE FIRST
    context = get_user_location_context(current_user.id)

    if context and context.get("awaiting_location"):
        try:
            set_user_location(current_user.id, request.message)

            task = allocate_task_from_chat(
                salesman_id=current_user.id,
                user_location=request.message,
                db=db
            )

            # 🔵 FIX: SAVE TRAVEL KM IN DAILY LOG
            travel_km = task.get("total_travel_km", 0.0)

            log = (
                db.query(DailySalesLog)
                .filter(
                    DailySalesLog.salesman_id == current_user.id,
                    DailySalesLog.work_date == date.today()
                )
                .first()
            )

            if not log:
                log = DailySalesLog(
                    salesman_id=current_user.id,
                    work_date=date.today(),
                    start_time=datetime.utcnow()
                )
                db.add(log)

            # 🔑 Accumulate travel for the day
            log.travel_km = (log.travel_km or 0.0) + travel_km

            db.commit()
            db.refresh(log)

            return ChatResponse(
                reply="📋 Here’s your optimized task plan for today.",
                data={
                    "route_assigned": task.get("route_assigned", []),
                    "assigned_products": task.get("assigned_products", []),
                    "summary": task.get("summary", {}),
                    "assigned_target": task.get("assigned_target", 0),
                    "tasks_pending": task.get("tasks_pending", 0)
                }
            )

        except ValueError:
            return ChatResponse(
                reply=(
                    "❌ I couldn’t recognize that location.\n"
                    "Try:\n"
                    "• Guindy Chennai\n"
                    "• OMR Chennai\n"
                    "• Near Tidel Park"
                )
            )

    # INTENT DETECTION
    intent = detect_intent(request.message)

    # SMALL TALK (ROLE AWARE)
    if intent == "SMALL_TALK":
        if current_user.role == "salesman":
            return ChatResponse(
                reply=(
                    f"👋 Hi {current_user.name}! I’m your Sales AI Assistant.\n\n"
                    "You can say:\n"
                    "• What is my task today?\n"
                    "• I have 3 pending items\n"
                    "• I am done for today"
                )
            )
        elif current_user.role == "manager":
            return ChatResponse(
                reply=(
                    f"👋 Hi {current_user.name}!\n\n"
                    "You can:\n"
                    "• View manager dashboard\n"
                    "• Assign teams & products\n"
                    "• Track sales performance"
                )
            )

    # GET DAILY TASK
    if intent == "GET_DAILY_TASK":
        set_waiting_for_location(current_user.id)
        return ChatResponse(
            reply="📍 Where are you right now? (Area or landmark)"
        )

    # END OF DAY REPORT
    if intent == "END_OF_DAY_REPORT":
        pending = extract_pending_items(request.message)

        if pending is None:
            return ChatResponse(
                reply=(
                    "🧾 Before closing your day, please tell me:\n"
                    "• How many items are pending?\n\n"
                    "Example:\n"
                    "👉 I have 3 pending items"
                )
            )

        total_target = get_salesman_daily_target(db, current_user.id)
        sold = max(total_target - pending, 0)

        log = (
            db.query(DailySalesLog)
            .filter(
                DailySalesLog.salesman_id == current_user.id,
                DailySalesLog.work_date == date.today()
            )
            .first()
        )

        if not log:
            log = DailySalesLog(
                salesman_id=current_user.id,
                work_date=date.today(),
                start_time=datetime.utcnow()
            )
            db.add(log)

        log.items_sold = sold
        log.items_pending = pending
        log.end_time = datetime.utcnow()

        db.commit()
        db.refresh(log)

        return ChatResponse(
            reply=(
                "✅ Day closed successfully!\n\n"
                f"📦 Target: {total_target}\n"
                f"✅ Sold: {sold}\n"
                f"⏳ Pending: {pending}\n\n"
                "Your work has been saved. See you tomorrow! 💪"
            )
        )

    # FALLBACK
    return ChatResponse(
        reply=(
            "🤔 I didn’t understand that.\n\n"
            "Try saying:\n"
            "• What is my task today?\n"
            "• I have 4 pending items\n"
            "• I am done for today"
        )
    )
