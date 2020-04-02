from typing import List
from fastapi import APIRouter, Request
from pydantic import BaseModel
from db import schemas

router = APIRouter()


@router.get("/")
async def root():
    return {"ack": "ok"}


class AnnotationCreate(BaseModel):
    class_id: int
    observation_id: int


class AnnotationRead(BaseModel):
    id: int
    class_id: int
    observation_id: int


@router.get("/annotations", response_model=List[AnnotationRead])
async def read_annotations(req: Request):
    db = req.app.state.db_client
    annotations = await db.fetch_all(schemas.annotations.select())
    return annotations


@router.post("/annotations", response_model=AnnotationRead)
async def create_annotation(anno: AnnotationCreate, req: Request):
    db = req.app.state.db_client
    query = schemas.annotations.insert().values(
        class_id=anno.class_id, observation_id=anno.observation_id
    )
    last_record_id = await db.execute(query)
    return {**anno.dict(), "id": last_record_id}


class ObservationCreate(BaseModel):
    text: str


class ObservationRead(BaseModel):
    id: int
    text: str


@router.get("/observations", response_model=List[ObservationRead])
async def read_observations(req: Request):
    db = req.app.state.db_client
    annotations = await db.fetch_all(schemas.observations.select())
    return annotations


@router.post("/observations", response_model=ObservationRead)
async def create_observations(obs: ObservationCreate, req: Request):
    db = req.app.state.db_client
    query = schemas.observations.insert().values(text=obs.text)
    last_record_id = await db.execute(query)
    return {**obs.dict(), "id": last_record_id}
