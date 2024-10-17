import os

MINIMUM_SCORE = os.getenv("MINIMUM_SCORE", 0.5)
SPEAKER_INDEX = os.getenv("SPEAKER_INDEX", "speaker-index")
IDENTIFIER = os.getenv("IDENTIFIER", "id")

DATABASE_HOST = os.getenv("DATABASE_HOST", f"{IDENTIFIER}.amazonaws.com")
REGION = os.getenv("REGION", "us-east-1")
SERVICE = os.getenv("SERVICE", "aoss")
DOMAIN = os.getenv("DOMAIN", "amazonaws.com")
