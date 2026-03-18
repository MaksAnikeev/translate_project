import redis.asyncio as redis
import logging


class RedisConnector:
    _redis: redis.Redis

    def __init__(self, host, port, password=None):
        self.port = port
        self.host = host
        self.password = password

    async def connect(self):
        logging.info(f"Начало подключение к Redis host: {self.host}, port: {self.port}")
        params = {"host": self.host, "port": self.port, "decode_responses": True}
        if self.password:
            params["password"] = self.password
            logging.info("Подключение к Redis с паролем")

        self._redis = await redis.Redis(**params)
        logging.info(f"Подключение к Redis успешно на host: {self.host}, port: {self.port}")

    async def set(self, key: str, value: str, expire: int = None):
        if expire:
            await self._redis.set(key, value, ex=expire)
        else:
            await self._redis.set(key, value)

    async def get(self, key: str):
        return await self._redis.get(key)

    async def delete(self, key: str):
        await self._redis.delete(key)

    async def close(self):
        if self._redis:
            await self._redis.close()
            logging.warning(f"Подключение к Redis закрыто")
