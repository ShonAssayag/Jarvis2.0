from datetime import datetime
from pydantic import BaseModel, field_validator
from src.databases.models import User


class Host(BaseModel):
    name: str
    dns: str
    resources: dict


class MongoDBHost(Host):
    port: int
    type: str  # standalone, replicaMember,config, mongos, shard0:replicaMember


class RedisHost(Host):
    pass


class Cluster(BaseModel):
    name: str
    env: str
    version: str
    creation_time: datetime
    last_update: datetime
    admin_credentials: User
    region: str
    responsible_team: str
    responsible_user: str

    @field_validator('creation_time', 'last_update', mode='before')
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )


class MongoDBCluster(Cluster):
    hosts: list[MongoDBHost]
    is_tls: bool
    auth_mechanism: str
    mms_group_id: str
    architecture: str
    databases: list[str]  # database_names


class RedisCluster(Cluster):
    hosts: list[RedisHost]
    total_memory: float
    allocated_memory: float
