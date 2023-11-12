from json import JSONEncoder

import uvicorn
from bson import ObjectId
from fastapi import FastAPI

from src.clusters.clusters_api import cluster_router


class ObjectIdJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return super().default(obj)


app = FastAPI()

app.json_encoder = ObjectIdJSONEncoder

app.include_router(cluster_router)


@app.get("/")
async def root():
    return "Nothing to see here:)"


if __name__ == '__main__':
    uvicorn.run(app, port=5000, host='0.0.0.0')
