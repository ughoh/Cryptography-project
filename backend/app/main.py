import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.api import router_v1
from app.core.config import settings

app = FastAPI(
    title=settings.app_settings.title,
    description=settings.app_settings.description,
    version=settings.app_settings.version,
)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=settings.cors.allow_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        return response


app.add_middleware(SecurityHeadersMiddleware)
app.include_router(router_v1)

if __name__ == "__main__":
    uvicorn.run(
        app=settings.app_run.app,
        host=settings.app_run.host,
        port=settings.app_run.port,
        reload=settings.app_run.reload,
    )
