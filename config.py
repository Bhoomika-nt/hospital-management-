import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # If you set DB_USER/DB_PASS/DB_NAME it will use MySQL, otherwise SQLite for quick run
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_NAME = os.environ.get('DB_NAME')

    if DB_USER and DB_PASS and DB_NAME:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital_hms.db'
