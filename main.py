import uvicorn
from config import Settings

global_settings = Settings()

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=global_settings.host,
        log_level=global_settings.log_level,
        reload=bool(global_settings.reload),
    )
