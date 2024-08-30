from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def redis_host_port(self):
        redis_host = self.REDIS_HOST
        redis_port = self.REDIS_PORT
        return redis_host, redis_port

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
