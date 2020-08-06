import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CSV PARAMS
    CSV_FILES_DIR = os.environ.get('CSV_FILES_DIR')
    CSV_FILE_FORMAT = "'CSV'"
