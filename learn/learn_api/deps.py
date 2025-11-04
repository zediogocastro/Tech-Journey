from fastapi import Depends

class FakeDBClient:
    def get_price(self, name):
        return 100 if name == "apple" else 200
    
async def get_client():
    return FakeDBClient()