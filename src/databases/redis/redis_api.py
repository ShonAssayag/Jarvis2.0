from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Body, HTTPException
import src.databases.redis.redis_database as redis_database
from src.databases.models import RedisDatabase

redis_database_router = APIRouter(prefix='/redis/database', tags=['Redis Database Actions'])


@redis_database_router.post('/')
async def add_database(database: RedisDatabase = Body(...)):
    try:
        result = redis_database.add_database(database.model_dump())
        if result:
            return PlainTextResponse(content="Database Added Successfully", status_code=200)
        else:
            return PlainTextResponse(
                content=f"One Of The Following Clusters: {database.participating_clusters} Does Not Exist",
                status_code=404)
    except HTTPException as e:
        return e


@redis_database_router.delete('/')
async def delete_database_by_name(cluster_name: str, database_name: str):
    try:
        database = redis_database.delete_database_by_name(cluster_name, database_name)
        if database:
            database['_id'] = str(database['_id'])
            return JSONResponse(content=jsonable_encoder(database), status_code=200)
        else:
            return PlainTextResponse(content="No Cluster Found", status_code=404)
    except HTTPException as e:
        return e


@redis_database_router.get('/')
async def get_database_by_name(cluster_name: str, database_name: str):
    try:
        database = redis_database.get_database_by_name(cluster_name, database_name)
        if database:
            database['_id'] = str(database['_id'])
            return JSONResponse(content=jsonable_encoder(database), status_code=200)
        else:
            return PlainTextResponse(content="No Cluster Found", status_code=404)
    except HTTPException as e:
        return e


@redis_database_router.get('/alias')
async def get_database_by_alias(alias_name: str):
    try:
        database = redis_database.get_database_by_alias(alias_name)
        if database:
            database['_id'] = str(database['_id'])
            return JSONResponse(content=jsonable_encoder(database), status_code=200)
        else:
            return PlainTextResponse(content="No Cluster Found", status_code=404)
    except HTTPException as e:
        return e
