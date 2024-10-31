from fastapi.responses import Response
from starlette.requests import Request

from src.api.router import router
from src.crypto import get_crypto

@router.post('/crypto')
async def crypto_webhook(request: Request) -> Response:
    await get_crypto().get_updates(request)