from datetime import datetime

class SingleDoUser:
    _instance = None
    do = {}
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def addDo(self, userId: int, do: str, date: datetime):
        self.do[userId] = { 
                "do" : do,
                "date" : date
            }

    def removeDo(self, userId: int):
        del self.do[userId]