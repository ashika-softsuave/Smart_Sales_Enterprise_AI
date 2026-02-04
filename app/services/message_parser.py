import re

def extract_pending_items(message: str) -> int | None:
    """
    Extract pending items count from natural language
    Examples:
    - '4 pending items'
    - 'pending 5'
    """
    match = re.search(r'(\d+)\s*(pending|left|remaining)', message.lower())
    if match:
        return int(match.group(1))
    return None
