from collections import defaultdict

class MessageStorage: 
    def __init__(self):
        self._storage = defaultdict(list)
    
    def add(self, user_id: int, message_id: int):
        self._storage[user_id].append(message_id)
    
    def get(self, user_id: int):
        return self._storage.get(user_id, [])
    
    def clear(self, user_id: int):
        self._storage[user_id] = []