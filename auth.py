# auth.py

# Simple in-memory user store
# You can change usernames/passwords/roles as needed.
USERS = {
    "admin1": {
        "password": "admin123",
        "role": "admin"
    },
    "faculty1": {
        "password": "fac123",
        "role": "faculty"
    },
    "faculty2": {
        "password": "fac456",
        "role": "faculty"
    },
    "student1": {
        "password": "stu123",
        "role": "student"
    },
    "student2": {
        "password": "stu456",
        "role": "student"
    }
}


def validate_user(username: str, password: str):
    """
    Check if username/password is valid.
    If valid → return role ('admin' / 'faculty' / 'student')
    If invalid → return None
    """
    user = USERS.get(username)
    if not user:
        return None

    if user["password"] == password:
        return user["role"]

    return None
