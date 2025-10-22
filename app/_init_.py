from .extensions import db
from dotenv import load_dotenv

load_dotenv()

from .user import User
from .crop import Crop
from .livestock import Livestock
from .disease import Disease
from .market import Market
from .weather import Weather
from .post import Post
from .notification import Notification
from .relations import CropDisease, LivestockDisease

__all__ = [
    "User",
    "Crop",
    "Livestock",
    "Disease",
    "Market",
    "Weather",
    "Post",
    "Notification",
    "CropDisease",
    "LivestockDisease",
]
