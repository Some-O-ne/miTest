from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Settings():
    key: str

settings = Settings(key=os.getenv('KEY'))