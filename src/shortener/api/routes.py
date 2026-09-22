from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

from shortener.api.dependencies import BaseUrlDep, ServiceDep
from shortener.api.schemas import LinkResponse, ShortenRequest

health_router = APIRouter(tags=["monitoring"])
links_router = APIRouter(prefix="/links", tags=["links"])
redirect_router = APIRouter(tags=["links"])


@health_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@links_router.post("", status_code=status.HTTP_201_CREATED)
async def shorten(
    payload: ShortenRequest, service: ServiceDep, base_url: BaseUrlDep
) -> LinkResponse:
    link = await service.shorten(str(payload.target_url))
    return LinkResponse.from_domain(link, base_url)


@links_router.get("/{code}")
async def stats(code: str, service: ServiceDep, base_url: BaseUrlDep) -> LinkResponse:
    link = await service.stats(code)
    return LinkResponse.from_domain(link, base_url)


@redirect_router.get("/{code}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect(code: str, service: ServiceDep) -> RedirectResponse:
    link = await service.resolve(code)
    return RedirectResponse(link.target_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
