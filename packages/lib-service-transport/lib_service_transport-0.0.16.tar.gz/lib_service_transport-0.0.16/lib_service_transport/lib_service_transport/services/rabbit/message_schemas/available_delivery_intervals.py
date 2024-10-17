from datetime import datetime
from datetime import time

from pydantic import BaseModel


class AvailableDeliveryIntervalIncomingMessage(BaseModel):
    sales_order_nrec: str


class AvailableDeliveryInterval(BaseModel):
    intervalNrec: str
    intervalNum: int
    deliveryDate: datetime
    timeFrom: time
    timeTo: time


class AvailableDeliveryIntervalOutgoingMessage(BaseModel):
    available_delivery_intervals: list[AvailableDeliveryInterval | None]
