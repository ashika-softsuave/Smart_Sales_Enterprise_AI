def format_daily_task_response(task_data:dict):
    return(
        f"📍 Your task for today:\n"
        f"🎯 Target:{task_data['assigned_target']}sales\n"
        f"🟢  Completed:{task_data['task_reached']}\n"
        f"🔴 Pending: {task_data['tasks_pending']}\n"
        f"🛣️ Distance: {task_data['route_assigned']['distance_km']} km\n"
        f"⏱️ Duration: {task_data['route_assigned']['duration_minutes']} mins"
    )