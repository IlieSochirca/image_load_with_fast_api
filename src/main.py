"""App Module where app configuration will resides"""
from src.api.service import Application


app = Application()
application = app.run()
