from aiogram import Router
from .subscription import router as subscription_router

router = Router()
router.include_router(subscription_router)
