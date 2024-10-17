from ninja import Router, Schema
from kitchenai_sdk.kitchenai import KitchenAIApp
import asyncio

from typing import Optional

router = Router()

class Item(Schema):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

kitchen = KitchenAIApp(router=router)

@kitchen.query("query-1")
def add(request, item: Item):
    return {"result is": item}


@kitchen.query("query-2")
async def kitchen(request):
    await asyncio.sleep(1)

    return {"result is": "ok"}