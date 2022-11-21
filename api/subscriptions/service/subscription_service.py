import os
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import random
from typing import List
from beanie import PydanticObjectId
from fastapi import Body, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi_pagination import Page, paginate

from api.subscriptions.schemas.subscriptions import Subscription

rImageP = f"{os.getcwd()}/api/subscriptions/image/LOGO-POS-GLOBAL-PNG.png"
rImageS = f"{os.getcwd()}/api/subscriptions/image/sunmi_logo.jpeg"


class SubscriptionService:
    async def pdf(self, name, number, cedula, apellido, telefono, correo):
        class PDF(FPDF):
            def header(self):

                self.ln(10)
                self.image(rImageP, x=65, y=-5, w=90, h=90)
                self.ln(15)

                self.image(rImageS, x=92, y=130, w=30, h=30)

                self.ln(24)
                self.set_font("helvetica", "", 23)
                # Move to the right
                self.cell(20)

                sliced_number = str(number)

                self.multi_cell(
                    w=150,
                    h=10,
                    txt=f"¡Felicidades, estás participando!\n Tu ID de sorteo es: {sliced_number[-8:]}",
                    border=0,
                    align="C",
                    fill=0,
                )

                self.ln()
                self.cell(20)
                self.cell(
                    w=150,
                    h=10,
                    txt=f"Nombre: {name} {apellido}",
                    border=0,
                    align="C",
                    fill=0,
                )

                self.ln()
                self.cell(20)

                self.set_font("helvetica", "", 22)
                self.cell(
                    w=150, h=10, txt=f"C.I: {cedula} ", border=0, align="C", fill=0
                )

                self.ln()
                self.cell(20)

                self.cell(
                    w=150,
                    h=10,
                    txt=f"Teléfono: {telefono}",
                    border=0,
                    align="C",
                    fill=0,
                )

                self.ln()
                self.cell(20)
                self.cell(
                    w=150, h=10, txt=f"Correo: {correo}", border=0, align="C", fill=0
                )

                self.ln(33)
                self.cell(55)
                self.set_font("arial", "B", 14)
                self.multi_cell(w=150, h=10, txt="Powered By Sunmi Corporation, C.A.")
                self.ln(5)

        pdf = PDF()

        pdf.add_page()

        ruta = f"{os.getcwd()}/pdf"
        os.makedirs(ruta, exist_ok=True)

        pdf.output(ruta + "/ticket.pdf")

        return ruta + "/ticket.pdf"

    async def subscribe(self, body: Subscription = Body(...)):
        existing_sub = await Subscription.find_one(Subscription.cedula == body.cedula)

        if not existing_sub:
            subscription = await body.create()
            pdf = await self.get_pdf_subscription(subscription.cedula)
            return pdf
        else:
            return JSONResponse(
                {"Message": "Este participante ya está registrado!!"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    async def get_all_subscriptions(self) -> Page[Subscription]:
        return await Subscription.find_all().to_list()

    async def get_one_subscription(self, cedula: str) -> Subscription:
        return await Subscription.find_one(Subscription.cedula == cedula)

    async def delete_subscription(self, id: PydanticObjectId) -> dict:
        sub = await Subscription.get(id)
        await sub.delete()
        return {"message": "Subscription deleted successfully"}

    async def get_pdf_subscription(self, cedula: str):
        subscriber_data = await self.get_one_subscription(cedula)
        if subscriber_data:
            pdf = await self.pdf(
                subscriber_data.name,
                subscriber_data.id,
                subscriber_data.cedula,
                subscriber_data.last_name,
                subscriber_data.phone,
                subscriber_data.mail,
            )
            headers = {"Content-Disposition": "inline"}
            return FileResponse(
                path=pdf,
                headers=headers,
                filename="ticket.pdf",
            )
        else:
            return JSONResponse(
                {"Message": "Participante no encontrado!!"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

    async def get_winner_subscription(self):
        subscriptions = await self.get_all_subscriptions()
        if len(subscriptions) > 0:
            num = random.randint(0, len(subscriptions) - 1)
            return subscriptions[num]
        else:
            return {"message": "No subscriptions to sort"}

    async def get_excel_subscriptions(self):
        excel_file_path = (
            f"{os.getcwd()}/api/subscriptions/excel_files/participantes.xlsx"
        )

        subscriptions = await self.get_all_subscriptions()

        # convert pydantic objects to dict
        subs = [item.dict() for item in subscriptions]

        # convert into dataframe
        df = pd.DataFrame(data=subs)

        # convert into excel
        df.to_excel(excel_file_path, index=False)

        headers = {"Content-Disposition": "inline"}

        return FileResponse(
            path=excel_file_path,
            headers=headers,
            media_type="application/xlsx",
            filename="participantes.xlsx",
        )
