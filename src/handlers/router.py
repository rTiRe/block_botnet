from aiogram import Router

from src.handlers.demolition import router as demolition_router
from src.handlers.subscription import router as subscription_router

router = Router()
router.include_routers(
    subscription_router,
    demolition_router,
)
