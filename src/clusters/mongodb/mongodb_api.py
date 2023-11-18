from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Body, HTTPException
import src.clusters.mongodb.mongodb_cluster as mongodb_cluster
from src.clusters.models import MongoDBCluster

mongodb_cluster_router = APIRouter(prefix='/mongodb/cluster', tags=['Make MongoDB Cluster Actions'])


@mongodb_cluster_router.post('/')
async def add_cluster(cluster: MongoDBCluster = Body(...)):
    try:
        mongodb_cluster.add_cluster(cluster.model_dump())
        return PlainTextResponse(content="Cluster Added Successfully", status_code=200)
    except HTTPException as e:
        return e


@mongodb_cluster_router.delete('/')
async def delete_cluster_by_name(name):
    try:
        cluster = mongodb_cluster.delete_cluster_by_name(name)
        if cluster:
            cluster['_id'] = str(cluster['_id'])
            return JSONResponse(content=jsonable_encoder(cluster), status_code=200)
        else:
            return PlainTextResponse(content="No Cluster Found", status_code=404)
    except HTTPException as e:
        return e


@mongodb_cluster_router.get('/')
async def get_cluster_by_name(name):
    try:
        cluster = mongodb_cluster.get_cluster_by_name(name)
        if cluster:
            cluster['_id'] = str(cluster['_id'])
            return JSONResponse(content=jsonable_encoder(cluster), status_code=200)
        else:
            return PlainTextResponse(content="No Cluster Found", status_code=404)
    except HTTPException as e:
        return e
