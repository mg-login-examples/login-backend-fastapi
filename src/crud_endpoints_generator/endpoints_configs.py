from typing import List, Any

class Configs:
    def __init__(self):
        self.add = False
        self.dependencies = []
    
    def require(self, dependencies: List[Any] = []):
        self.add = True
        self.dependencies.extend(dependencies)

class EndpointsConfigs:
    def __init__(self):
        self.get_items_count = Configs()
        self.get_items = Configs()
        self.get_item = Configs()
        self.post_item = Configs()
        self.put_item = Configs()
        self.delete_item = Configs()
        self.sql_db = True

    def require_all(self, dependencies: List[Any] = []):
        self.get_items_count.require(dependencies)
        self.get_items.require(dependencies)
        self.get_item.require(dependencies)
        self.post_item.require(dependencies)
        self.put_item.require(dependencies)
        self.delete_item.require(dependencies)
        return self
    
    def resource_in_sql_db(self):
        self.sql_db = True

    def resource_in_mongo_db(self):
        self.sql_db = False

    def require_get_items_count(self, dependencies: List[Any] = []):
        self.get_items_count.require(dependencies)
        return self

    def require_get_items(self, dependencies: List[Any] = []):
        self.get_items.require(dependencies)
        return self

    def require_get_item(self, dependencies: List[Any] = []):
        self.get_item.require(dependencies)
        return self

    def require_post_item(self, dependencies: List[Any] = []):
        self.post_item.require(dependencies)
        return self

    def require_put_item(self, dependencies: List[Any] = []):
        self.put_item.require(dependencies)
        return self

    def require_delete_item(self, dependencies: List[Any] = []):
        self.delete_item.require(dependencies)
        return self
