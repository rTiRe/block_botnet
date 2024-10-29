from fastapi.responses import ORJSONResponse
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api.router import router

@router.post('/crypto')
async def crypto_webhook(request: Request) -> JSONResponse:
    return ORJSONResponse({'message': 'Hello'})