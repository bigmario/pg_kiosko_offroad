import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import random
from typing import List
from beanie import PydanticObjectId
from beanie.operators import Or
from fastapi import Body, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi_pagination import Page, paginate

from api.subscriptions.schemas.subscriptions import Subscription

rImage = f"{os.getcwd()}/api/subscriptions/image/LOGO-POS-GLOBAL-PNG.png"


class SubscriptionService:
    async def pdf(self, name, number):
        class PDF(FPDF):
            def header(self):
                # Arial bold 15
                self.image(rImage, x=10, y=-2, w=200, h=170)
                self.ln(22)
                self.set_font("helvetica", "B", 10)
                # Move to the right
                self.cell(20)
                # marco
                self.set_font("helvetica", "B", 16)
                self.multi_cell(
                    w=150,
                    h=10,
                    txt=f'"Felicidades {name}, estas participando" \n Tu número: {number}',
                    border=0,
                    align="C",
                    fill=0,
                )
                self.cell(50)
                self.set_font("helvetica", "", 10)
                self.ln(5)

        pdf = PDF()

        pdf.add_page()

        ruta = f"{os.getcwd()}/pdf"
        os.makedirs(ruta, exist_ok=True)

        pdf.output(ruta + "/table_with_cells.pdf")

        return ruta + "/table_with_cells.pdf"

    async def subscribe(self, body: Subscription = Body(...)):
        existing_sub = await Subscription.find_one(Subscription.mail == body.cedula)

        if not existing_sub:
            subscription = await body.create()
            ticket = await self.get_pdf_subscription(subscription.id)
            return ticket
        else:
            return JSONResponse(
                {"Message": "Este participante ya está registrado!!"},
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
        subscriber_data = await self.get_one_subscription(id)
        pdf = await self.pdf(subscriber_data.name, subscriber_data.id)
        return FileResponse(
            pdf,
            media_type="application/octet-stream",
            content_disposition_type="inline",
        )

    async def get_winner_subscription(self):
        subscriptions = await self.get_all_subscriptions()
        num = random.randint(0, len(subscriptions) - 1)
        return subscriptions[num]
