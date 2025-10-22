import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres.lyrlnmcbnywkbovjwuqc:sBGWpCK4aHJlm26j@aws-1-eu-north-1.pooler.supabase.com:5432/postgres",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    