from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Body, HTTPException
from starlette.responses import PlainTextResponse

import src.clusters.redis.redis_cluster as redis_cluster
from src.clusters.models import RedisCluster

redis_cluster_router = APIRouter(prefix='/redis/cluster', tags=['Redis Cluster Actions'])


@redis_cluster_router.post('/')
async def add_cluster(cluster: RedisCluster = Body(...)):
    try:
        redis_cluster.add_cluster(cluster.model_dump())
        return "Cluster Added Successfully"
    except HTTPException as e:
        return e


@redis_cluster_router.delete('/')
async def delete_cluster_by_name(name):
    cluster = redis_cluster.delete_cluster_by_name(name)
    if cluster:
        cluster['_id'] = str(cluster['_id']) 
        return JSONResponse(content=jsonable_encoder(cluster), status_code=200)
    else:
        return PlainTextResponse(content="No Cluster Found", status_code=404)


@redis_cluster_router.get('/')
async def get_cluster_by_name(name):
    try:
        cluster = redis_cluster.get_cluster_by_name(name)
        if cluster:
            cluster['_id'] = str(cluster['_id'])
            return JSONResponse(content=jsonable_encoder(cluster), status_code=200)
        else:
            return PlainTextResponse(content="No Cluster Found", status_code=404)
    except HTTPException as e:
        return e
