"""Postgres DB configuration file"""
import os
from urllib.parse import quote_plus

import databases
import pydantic
import sqlalchemy
from sqlalchemy_utils import URLType

host_server = os.getenv("POSTGRES_HOST", "localhost")
database_port = os.getenv("POSTGRES_PORT", 5432)
database_name = os.getenv("POSTGRES_NAME", "fastapi")
database_username = quote_plus(str(os.getenv("POSTGRES_USER", "postgres")))
database_password = quote_plus(str(os.getenv("POSTGRES_PASSWORD", "secret")))
ssl_mode = quote_plus(str(os.getenv("SSL_MODE", "prefer")))

DATABASE_URL = f"postgresql://{database_username}:{database_password}@" \
               f"{host_server}:{database_port}/{database_name}?sslmode={ssl_mode}"

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=3)

database = databases.Database(DATABASE_URL)

photo = sqlalchemy.Table(
    "photo",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("description", sqlalchemy.String(50)),
    sqlalchemy.Column("image", URLType)
)


class Photo(pydantic.BaseModel):
    """Class that is responsible for data validation"""
    id: int
    name: str
    description: str
    image: pydantic.HttpUrl
