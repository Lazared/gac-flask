from os import environ

# Getting the Eviromental variables for a given config set
MYSQL_DB = environ.get("MYSQL_DB")
MYSQL_HOST = environ.get("MYSQL_HOST")
MYSQL_U_PWD = environ.get("MYSQL_U_PWD")
MYSQL_USER = environ.get("MYSQL_USER")


SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# API section
API_KEY = environ.get("API_KEY")
SECRET_KEY = environ.get("SECRET_KEY")