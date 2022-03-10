
class Endpoints:
    def __init__(self):
        self.get_items_count = False
        self.get_items = False
        self.get_item = False
        self.post_item = False
        self.put_item = False
        self.delete_item = False

    def require_all(self):
        self.get_items_count = True
        self.get_items = True
        self.get_item = True
        self.post_item = True
        self.put_item = True
        self.delete_item = True
        return self

    def require_get_items_count(self):
        self.get_items_count = True
        return self

    def require_get_items(self):
        self.get_items = True
        return self

    def require_get_item(self):
        self.get_item = True
        return self

    def require_post_item(self):
        self.post_item = True
        return self

    def require_put_item(self):
        self.put_item = True
        return self

    def require_delete_item(self):
        self.delete_item = True
        return self
