class MessageStorage:
    def __init__(self):
        self.data = {}

    def add(self, user_id: int, message_id: int):
        if user_id not in self.data:
            self.data[user_id] = []
        self.data[user_id].append(message_id)

    def get(self, user_id: int):
        return self.data.get(user_id, [])

    def clear(self, user_id: int):
        self.data[user_id] = []

message_storage = MessageStorage()