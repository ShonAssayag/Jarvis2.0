from datetime import datetime
from pydantic import BaseModel, field_validator


class Cluster(BaseModel):
    name: str
    env: str
    version: str
    creation_time: datetime
    last_update: datetime
    admin_credentials: dict
    region: str
    hosts: list[dict]

    @field_validator('creation_time', 'last_update', mode='before')
    def parse_birthdate(cls, value):
        return datetime.strptime(
            value,
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )


class MongoDBCluster(Cluster):
    is_tls: bool
    auth_mechanism: str
    mms_group_id: str
    architecture: str
    databases: list[dict]


class RedisCluster(Cluster):
    total_memory: float
    allocated_memory: float
