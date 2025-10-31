# app/messaging/producer.py
import asyncio
import json
from typing import Any
from aio_pika import connect_robust, Message, ExchangeType
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel

RABBIT_URL = "amqp://guest:guest@rabbit:5672/"  # в докере хост = service name 'rabbit'

class Producer:
    def __init__(self):
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractRobustChannel | None = None
        self._exchange_name = "app.events"

    async def connect(self):
        if self._connection and not self._connection.is_closed:
            return
        self._connection = await connect_robust(RABBIT_URL)
        self._channel = await self._connection.channel(publisher_confirms=True)
        # убедимся, что exchange существует
        await self._channel.declare_exchange(self._exchange_name, ExchangeType.TOPIC, durable=True)

    async def close(self):
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()

    async def publish(self, routing_key: str, payload: dict[str, Any]):
        if not self._channel:
            raise RuntimeError("Producer is not connected")
        exchange = await self._channel.get_exchange(self._exchange_name)
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        message = Message(body, content_type="application/json", delivery_mode=2)  # persistent
        await exchange.publish(message, routing_key=routing_key)

producer = Producer()