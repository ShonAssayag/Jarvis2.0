from json import JSONEncoder

from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Request, Body, HTTPException
import src.clusters.clusters_dal as clusters_dal

from src.clusters.clusters_dal import Cluster

cluster_router = APIRouter(prefix='/clusters', tags=['Make Cluster Actions'])


@cluster_router.post('/')
async def add_cluster(cluster: Cluster = Body(...)):
    try:
        clusters_dal.add_cluster(cluster.to_json())
        return "Cluster Added Successfully"
    except HTTPException as e:
        return e


@cluster_router.delete('/')
async def delete_cluster_by_name(name):
    clusters_dal.delete_cluster_by_name(name)


@cluster_router.get('/')
async def get_cluster_by_name(name):
    try:
        return JSONResponse(content=jsonable_encoder(clusters_dal.get_cluster_by_name(name)))
    except HTTPException as e:
        return e
