from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

cloudinary.config(
    cloud_name=os.getenv("Monopoly_game "),
    api_key=os.getenv("669932343378715"),
    api_secret=os.getenv("LCzvNXOHTfR_4TZBINRNz3EZzuc")
)