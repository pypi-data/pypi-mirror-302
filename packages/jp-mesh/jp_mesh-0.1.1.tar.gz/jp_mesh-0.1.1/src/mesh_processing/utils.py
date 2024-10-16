import time
from functools import wraps

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper

def format_log_message(prefix: str, data: dict) -> str:
    """
    Format a log message with aligned key-value pairs.
    
    Args:
    prefix (str): Prefix for the log message (e.g., [ORIGINAL] or [SIMPLIFIED]).
    data (dict): Dictionary of key-value pairs to log.
    
    Returns:
    str: Formatted log message.
    """
    max_key_length = max(len(key) for key in data.keys())
    formatted_lines = [f"{prefix}"]
    for key, value in data.items():
        if isinstance(value, float):
            formatted_value = f"{value:.4f}"
        else:
            formatted_value = str(value)
        formatted_lines.append(f"  {key.ljust(max_key_length)} : {formatted_value}")
    return "\n".join(formatted_lines)
