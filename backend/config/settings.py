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
