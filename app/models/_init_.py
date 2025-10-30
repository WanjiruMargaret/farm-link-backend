from extensions import db
from dotenv import load_dotenv

load_dotenv()

# Import all models AFTER db is imported
from .user import User
from .crop import Crop
from .livestock import Livestock
from .disease import Disease
from .market import Market
from .weather import Weather
from .post import Post
from .notification import Notification
from .relations import CropDisease, LivestockDisease

User.crops = db.relationship('Crop', backref='user', lazy=True)
User.livestock = db.relationship('Livestock', back_populates='user', lazy=True)
User.posts = db.relationship('Post', back_populates='user', lazy=True)
User.notifications = db.relationship('Notification', backref='user', lazy=True)
User.market_items = db.relationship('Market', back_populates='seller', lazy=True)


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
