from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str
    log_level: str
    reload: int
    db_name: str
    mongo_root_username: str
    mongo_root_password: str
    mongo_db_host: str
    mongo_db_port: int

    class Config:
        env_file = ".env"
