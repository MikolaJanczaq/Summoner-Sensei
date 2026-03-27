import os

from dotenv import load_dotenv

load_dotenv()

PATCH_VERSION = os.getenv('PATCH_VERSION')
BASE_URL = os.getenv('BASE_URL').format(patch_version=PATCH_VERSION)
