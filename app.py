from json import JSONEncoder

import uvicorn
from bson import ObjectId
from fastapi import FastAPI

from src.clusters.mongodb.mongodb_api import mongodb_cluster_router
from src.clusters.redis.redis_api import redis_cluster_router
from src.databases.mongodb.mongodb_api import mongodb_database_router


class ObjectIdJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return super().default(obj)


app = FastAPI()

app.json_encoder = ObjectIdJSONEncoder

app.include_router(mongodb_cluster_router)
app.include_router(mongodb_database_router)
app.include_router(redis_cluster_router)


@app.get("/")
async def root():
    return "Nothing To See Here:)"


if __name__ == '__main__':
    uvicorn.run(app, port=5000, host='0.0.0.0')
