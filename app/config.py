import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_key")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "mydatabase")
    DB_USER = os.getenv("DB_USER", "myuser")
    DB_PASS = os.getenv("DB_PASS", "mypassword")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail Config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "your_email@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "your_app_password_here")

    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')  # read from env


    # Frontend
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
