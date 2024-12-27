from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8000
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    
    # Distributed system settings
    WORKER_COUNT: int = 3
    BATCH_SIZE: int = 100
    QUEUE_TIMEOUT: int = 30

settings = Settings()