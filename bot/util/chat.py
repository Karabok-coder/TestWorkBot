class SingleChat:
    _instance = None
    chats = []
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def addChat(self, userId: int, managerId: int):
        self.chats.append((userId, managerId))

    def closeChat(self, userId: int, managerId: int):
        self.chats.remove((userId, managerId))