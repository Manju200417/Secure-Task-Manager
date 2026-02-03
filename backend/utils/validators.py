import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    # At least 6 characters
    return len(password) >= 6

def validate_task_data(title, description):
    if not title or title.strip() == "":
        return False, "Title cannot be empty"
    
    if len(title) > 200:
        return False, "Title too long"
    
    return True, ""