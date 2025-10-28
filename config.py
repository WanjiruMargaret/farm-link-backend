import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres.lyrlnmcbnywkbovjwuqc:sBGWpCK4aHJlm26j@aws-1-eu-north-1.pooler.supabase.com:5432/postgres",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    CLOUDINARY_CLOUD_NAME = os.getenv("Monopoly_game")
    CLOUDINARY_API_KEY = os.getenv("669932343378715")
    CLOUDINARY_API_SECRET = os.getenv("LCzvNXOHTfR_4TZBINRNz3EZzuc")
    GEMINI_API_KEY = os.getenv("AIzaSyDoSIJcxUyyAddM54Nd13iSW8UDsy-vhIs")
    