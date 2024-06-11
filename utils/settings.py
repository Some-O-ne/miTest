from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Settings():
    key: str
    DBName: str

settings = Settings(key=os.getenv('KEY'),DBName="test.db")