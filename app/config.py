from pydantic import BaseConfig


class Config(BaseConfig):
    #JWT
    SECRET_KEY = "asash19efwkfnjsafjkwebjkccjknew"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


config = Config()