import os
from dotenv import load_dotenv

load_dotenv()

IMAGES_COUNT = os.getenv("IMAGES_COUNT")
IMAGE_TARGET_SIZE = os.getenv("IMAGE_TARGET_SIZE")