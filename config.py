import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_URL = os.path.join(BASE_DIR, "sync.db")

SECRET_KEY = "sync_secret_key_2026"