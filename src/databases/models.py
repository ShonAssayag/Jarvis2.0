from datetime import datetime
from pydantic import BaseModel, field_validator


class Role(BaseModel):
    name: str


class RedisRole(Role):
    cluster_role: str
    acl: str


class MongoDBRole(Role):
    auth_database: str
    permissions: list[str]


class User(BaseModel):
    username: str
    password: str


class MongoDBUser(User):
    auth_database: str
    roles: list[MongoDBRole]


class RedisUser(User):
    role: RedisRole


class Database(BaseModel):
    name: str
    creation_time: datetime
    last_update: datetime

    @field_validator('creation_time', 'last_update', mode='before')
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )


class MongoDBDatabase(Database):
    users: list[MongoDBUser]


class RedisDatabase(Database):
    id: str
    max_memory: float
    num_shards: int
    replication: bool
    port: int
    crdb: bool
    participating_clusters: list[str]  # cluster_name
    users: list[RedisUser]
