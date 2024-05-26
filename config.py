import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:root_pass@localhost/keijiban')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    SQLALCHEMY_ECHO = True  # クエリをログに出力するための設定
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # セキュアなキーを設定してください