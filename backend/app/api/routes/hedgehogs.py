from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.hedgehogs import HedgehogsRepository
from app.models.hedgehog import HedgehogCreate, HedgehogPublic
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

router = APIRouter()


@router.get("/")
async def get_all_hedgehogs() -> List[dict]:
    hedgehogs = [
        {"id": 1, "name": "momo", "color": "SALT & PEPPER", "age": 2},
        {"id": 2, "name": "coco", "color": "DARK GREY", "age": 1.5}
    ]

    return hedgehogs


@router.post("/",
             response_model=HedgehogPublic,
             name="hedgehogs:create-hedgehog",
             status_code=HTTP_201_CREATED)
async def create_new_hedgehog(
    new_hedgehog: HedgehogCreate = Body(..., embed=True),
    hedgehogs_repo: HedgehogsRepository = Depends(get_repository(HedgehogsRepository)),
) -> HedgehogPublic:
    created_hedgehog = await hedgehogs_repo.create_hedgehog(new_hedgehog=new_hedgehog)
    return created_hedgehog


@router.get("/{id}/", response_model=HedgehogPublic,
            name="hedgehogs:get-hedgehog-by-id")
async def get_hedgehog_by_id(
    id: int, hedgehogs_repo: HedgehogsRepository = Depends(
        get_repository(HedgehogsRepository
                       ))
) -> HedgehogPublic:
    hedgehog = await hedgehogs_repo.get_hedgehog_by_id(id=id)
    if not hedgehog:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="指定されたidのハリネズミは見つかりませんでした")
    return hedgehog
