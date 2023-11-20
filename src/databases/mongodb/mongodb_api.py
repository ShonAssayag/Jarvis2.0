from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Body, HTTPException
import src.databases.mongodb.mongodb_database as mongodb_database
from src.databases.models import MongoDBDatabase

mongodb_database_router = APIRouter(prefix='/mongodb/database', tags=['MongoDB Database Actions'])


@mongodb_database_router.post('/')
async def add_database(cluster_name: str, database: MongoDBDatabase = Body(...)):
    try:
        result = mongodb_database.add_database(cluster_name, database.model_dump())
        if result:
            return PlainTextResponse(content="Database Added Successfully", status_code=200)
        else:
            return PlainTextResponse(content=f"Cluster: {cluster_name} Does Not Exist", status_code=404)
    except HTTPException as e:
        return e


@mongodb_database_router.delete('/')
async def delete_database_by_name(cluster_name: str, database_name: str):
    try:
        database = mongodb_database.delete_database_by_name(cluster_name, database_name)
        if database:
            database['_id'] = str(database['_id'])
            return JSONResponse(content=jsonable_encoder(database), status_code=200)
        else:
            return PlainTextResponse(content="No Cluster Found", status_code=404)
    except HTTPException as e:
        return e


@mongodb_database_router.get('/')
async def get_database_by_name(cluster_name: str, database_name: str):
    try:
        database = mongodb_database.get_database_by_name(cluster_name, database_name)
        if database:
            database['_id'] = str(database['_id'])
            return JSONResponse(content=jsonable_encoder(database), status_code=200)
        else:
            return PlainTextResponse(content="No Cluster Found", status_code=404)
    except HTTPException as e:
        return e
