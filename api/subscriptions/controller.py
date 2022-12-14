from typing import List
from beanie import PydanticObjectId
from fastapi import (
    APIRouter,
    Header,
    Body,
    status,
    Path,
    HTTPException,
    Depends,
)
from fastapi.responses import FileResponse
from fastapi_pagination import Page, paginate

from api.error_handlers.schemas.bad_gateway import BadGatewayError
from api.error_handlers.schemas.not_found import NotFoundError
from api.error_handlers.schemas.unauthorized import UnauthorizedError
from api.utils.remove_422 import remove_422

from .schemas.subscriptions import Subscription
from .service.subscription_service import SubscriptionService

from .config import Settings

conf = Settings()

########################
# Subscription Router
########################
subscription_router = APIRouter(
    tags=["Subscription"],
    responses={
        status.HTTP_502_BAD_GATEWAY: {"model": BadGatewayError},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedError},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
    },
)

########################
# Create a subscription
########################
@subscription_router.post(
    path="/subscription",
    status_code=status.HTTP_201_CREATED,
    summary="Subscribe",
    response_class=FileResponse,
    response_model_exclude_unset=True,
)
@remove_422
async def subscribe(
    body: Subscription = Body(...),
    token: str = Header(),
    subscription_service: SubscriptionService = Depends(),
):
    """
    Subscribe:
    """
    if token == conf.secret:
        return await subscription_service.subscribe(body)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unauthorized!"
        )


########################
# GET ALL SUBSCRIPTIONS
########################
@subscription_router.get(
    path="/subscription",
    status_code=status.HTTP_200_OK,
    summary="Get All Subscriptions",
    response_model=Page[Subscription],
    response_model_exclude_unset=True,
)
@remove_422
async def get_all_subscriptions(
    subscription_service: SubscriptionService = Depends(),
) -> Page[Subscription]:
    try:
        subscriptions = await subscription_service.get_all_subscriptions()
        return paginate(subscriptions)
    except Exception as e:
        return f"An exception occurred: {e}"


#################################
# GET ALL SUBSCRIPTIONS ON EXCEL
#################################
@subscription_router.get(
    path="/subscription/excel",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
    summary="Get All Subscriptions on Excel",
)
@remove_422
async def get_excel_subscriptions(
    subscription_service: SubscriptionService = Depends(),
):
    return await subscription_service.get_excel_subscriptions()


#############################
# SELECT RANDOM SUBSCRIPTION
#############################
@subscription_router.get(
    path="/subscription/winner",
    status_code=status.HTTP_200_OK,
    summary="Get Winner Subscription",
    response_model_exclude_unset=True,
)
@remove_422
async def get_winner_subscription(
    subscription_service: SubscriptionService = Depends(),
):
    winner_subscription = await subscription_service.get_winner_subscription()
    return winner_subscription


#############################
# GET ONE SUBSCRIPTION BY ID
#############################
@subscription_router.get(
    path="/subscription/{cedula}",
    status_code=status.HTTP_200_OK,
    summary="Get One Subscription By Cedula",
    response_model=Subscription,
    response_model_exclude_unset=True,
)
@remove_422
async def get_one_subscription(
    cedula: str = Path(...),
    subscription_service: SubscriptionService = Depends(),
) -> Subscription:
    subscription = await subscription_service.get_one_subscription(cedula)
    if subscription:
        return subscription
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Participante no encontrado!"
        )


#############################
# DELETE SUBSCRIPTION BY ID
#############################
# @subscription_router.delete(
#     path="/subscription/{id}",
#     status_code=status.HTTP_200_OK,
#     summary="Delete One Subscription By ID",
#     response_model_exclude_unset=True,
# )
# @remove_422
# async def delete_subscription(
#     id: PydanticObjectId = Path(...),
#     subscription_service: SubscriptionService = Depends(),
# ) -> dict:
#     try:
#         return await subscription_service.delete_subscription(id)
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"Subscription not found!"
#         )


#############################
# GET PDF BY SUBSCRIPTION ID
#############################
@subscription_router.get(
    path="/subscription/pdf/{cedula}",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
    summary="Get PDF By Subscription ID",
)
@remove_422
async def get_pdf_subscription(
    cedula: str = Path(...),
    subscription_service: SubscriptionService = Depends(),
):
    return await subscription_service.get_pdf_subscription(cedula)
