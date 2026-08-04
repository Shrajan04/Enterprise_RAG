# ================================================================
# File: settings.py
#
# Purpose:
# Stores all application configuration in one place.
#
# Responsibilities:
# - Reads values from the .env file.
# - Stores application settings like:
#     - App Name
#     - App Version
#     - Debug Mode
#     - Database Credentials
# - Provides a single settings object that can be used
#   throughout the project.
#
# Benefit:
# Avoids hardcoding configuration values in multiple files.
# ================================================================

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    app_version: str
    debug: bool

    #database
    
    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str

    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


settings = Settings()
