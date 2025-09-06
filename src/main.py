import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from loguru import logger


sys.path.append(str(Path(__file__).parent.parent))

from src.api.resume import router as resume_router
from src.api.auth import router as auth_router

app = FastAPI()

origins = [
    "http://localhost:3000",  # фронт
    "http://127.0.0.1:3000",  # иногда полезно

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # можно ["*"] для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(resume_router)
app.include_router(auth_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(
        f"Response status: {response.status_code} for {request.method} {request.url}"
    )
    return response


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
