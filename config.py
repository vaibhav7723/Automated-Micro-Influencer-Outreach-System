import os

DISCOVERY_MODE = os.getenv("DISCOVERY_MODE", "demo")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SENDER_NAME = os.getenv("SENDER_NAME", "EDXSO Partnerships")
DRY_RUN = os.getenv("DRY_RUN", "true").lower() != "false"

MIN_FOLLOWERS = 5_000
MAX_FOLLOWERS = 100_000
MIN_ENGAGEMENT_RATE = 1.5

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
INFLUENCER_CSV = os.path.join(DATA_DIR, "influencers.csv")
TRACKER_DB = os.path.join(DATA_DIR, "outreach_tracker.db")
TRACKER_CSV = os.path.join(DATA_DIR, "outreach_tracker.csv")
MESSAGES_CSV = os.path.join(DATA_DIR, "personalized_messages.csv")

NICHES = ["Fitness", "Fintech", "Beauty", "Fashion", "Technology"]
