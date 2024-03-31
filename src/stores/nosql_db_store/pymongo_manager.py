import logging

from pymongo import MongoClient
from pymongo.database import Database
from pymongo_inmemory import MongoClient as MongoClientInMemory  # type: ignore

logger = logging.getLogger(__name__)


class PyMongoManager:
    def __init__(
        self,
        mongo_host: str,
        mongo_port: int,
        mongo_username: str,
        mongo_password: str,
        mongo_database: str,
        use_in_memory_mongo_db: bool = False
    ):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_username = mongo_username
        self.mongo_password = mongo_password
        self.mongo_database = mongo_database
        self.use_in_memory_mongo_db = use_in_memory_mongo_db
        self.client: MongoClient | MongoClientInMemory | None = None
        self.db: Database | None = None

    def get_db(self) -> Database | None:
        if self.db is None:
            self.init_mongodb_client()
        return self.db

    def assert_mongo_db_is_available(self):
        try:
            if self.client is None:
                self.init_mongodb_client()
            assert self.client is not None
            self.client.server_info()
            logger.info("Test mongo db connection established successfully")
        except Exception as e:
            logger.error("Error pinging to mongo")
            raise Exception(
                "Mongo connection refused. You may need to launch a mongo db. Run `./scripts_docker.sh launch-databases`") from None

    def init_mongodb_client(self):
        # TODO Check if new client / db should be generated for each request, or same can be used
        # Note: When using pymongo_inmemory, same client & db should be used
        # otherwise new local mongodb instance is created everytime
        # MongoClientInMemory() is called
        if not self.use_in_memory_mongo_db:
            client: MongoClient | MongoClientInMemory = MongoClient(
                self.mongo_host,
                self.mongo_port,
                username=self.mongo_username,
                password=self.mongo_password,
            )
        else:
            # Starts a local MongoDb server, and stops when the app is closed
            # Data is not persisted on app restart
            # Should be used only for local development
            client = MongoClientInMemory()
        self.client = client
        self.db = client[self.mongo_database]
