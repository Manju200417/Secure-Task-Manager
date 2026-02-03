import os

class Config:
    SECRET_KEY = "my_super_secure_key_2026_with_extra_entropy_!@#_change_me"  # In real projects, use environment variables
    DATABASE_PATH = "users.db"
    JWT_EXPIRY_HOURS = 24
    LOG_FILE = "logs/app.log"