from beanie import init_beanie
import motor.motor_asyncio

from config import Settings
from api.subscriptions.schemas import Subscription

conf = Settings()


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{conf.mongo_root_username}:{conf.mongo_root_password}@{conf.mongo_db_host}:{conf.mongo_db_port}"
    )

    await init_beanie(database=client.db_name, document_models=[Subscription])
