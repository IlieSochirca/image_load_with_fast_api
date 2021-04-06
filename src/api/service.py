"""Service App definition"""
import logging
import os

import cloudinary
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.views import router
from src.api.db import engine, database, metadata

logger = logging.getLogger(__name__)


class Application:
    """Main Application Class Definition.
    This Class contains all the application initial setup configuration that is run on app start up
    """

    def __init__(self):
        cloudinary.config(
            cloud_name=os.getenv("CLOUD_NAME"),
            api_key=os.getenv("CLOUD_API_KEY"),
            api_secret=os.getenv("CLOUD_API_SECRET")
        )

    def run(self):
        """This method contains the initial setup configuration that is run on app start up"""
        metadata.create_all(engine)

        app = FastAPI()

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

        async def connect_to_db():
            """
            Callback that will create a connection pool to the database on app start up
            """
            try:
                app.state.db = database
                await database.connect()
            except Exception as e:
                logger.warning("--- DB CONNECTION ERROR ---")
                logger.warning(e)
                logger.warning("--- DB CONNECTION ERROR ---")

        async def close_db_connection():
            """
            Callback that will close the connection pool to the database on app shutdown
            """
            try:
                await database.disconnect()
            except Exception as e:
                logger.warning("--- DB DISCONNECT ERROR ---")
                logger.warning(e)
                logger.warning("--- DB DISCONNECT ERROR ---")

        app.include_router(router, prefix="/api/v1/photos")

        app.add_event_handler("startup", connect_to_db)
        app.add_event_handler("shutdown", close_db_connection)

        return app
