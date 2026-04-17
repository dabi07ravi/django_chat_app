class MongoUser:
    def __init__(self, user_data):
        self.user_data = user_data
        self._id = str(user_data["_id"])

    @property
    def is_authenticated(self):
        return True

    def __getitem__(self, key):
        return self.user_data.get(key)