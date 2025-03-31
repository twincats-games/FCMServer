import os
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

# 🔹 Logging Config
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "fcm_server.log")
LOG_MAX_SIZE = 100 * 1024 * 1024  # 100MB
LOG_RETENTION_DAYS = 7

# 🔹 Database Config (uses ENV or defaults)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@db/fcm_db")

# 🔹 Security Settings
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")  # For JWT/Auth
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# 🔹 Rate Limiting (Anti-DDOS)
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", 100))  # Max requests per window
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 60))  # Time window in seconds

# 🔹 Allowed Hosts (CORS Protection)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "https://services-twincats.ddns.net").split(",")

# 🔹 API Prefix
API_PREFIX = "/api/v1"
