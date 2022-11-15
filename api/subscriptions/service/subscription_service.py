import os
import random
from typing import List
from beanie import PydanticObjectId
from beanie.operators import Or
from fastapi import Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, paginate

from api.subscriptions.schemas.subscriptions import Subscription


class SubscriptionService:
    async def subscribe(self, body: Subscription = Body(...)):
        existing_sub = await Subscription.find_one(Subscription.mail == body.mail)

        if not existing_sub:
            await body.create()
            return JSONResponse(
                {"Message": "Subscribed!!"},
                status_code=status.HTTP_201_CREATED,
            )
        else:
            return JSONResponse(
                {"Message": "Duplicate Email!!"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    async def get_all_subscriptions(self) -> Page[Subscription]:
        return await Subscription.find_all().to_list()

    async def get_one_subscription(self, id: PydanticObjectId) -> Subscription:
        return await Subscription.get(id)

    async def delete_subscription(self, id: PydanticObjectId) -> dict:
        sub = await Subscription.get(id)
        await sub.delete()
        return {"message": "Subscription deleted successfully"}

    async def get_pdf_subscription(self, id: PydanticObjectId):
        subscriber_data = self.get_one_subscription(id)
        return subscriber_data
        # con subscriber_data se alimenta el metodo de generar pdf

    async def get_winner_subscription(self):
        subscriptions = await self.get_all_subscriptions()
        num = random.randint(0, len(subscriptions) - 1)
        return subscriptions[num]
