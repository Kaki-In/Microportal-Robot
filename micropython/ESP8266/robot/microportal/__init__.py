import uasyncio as _asyncio
import uwebsocket as _wetbsocket
import ujson as _json
from .actions import *

class MicroportalConnection():
    LIST = RobotActionsList()
    
    def __init__(self, addr, name, host, post):
        self._conn = None
        self._addr = addr
        self._name = name
        self._host = host
        self._port = port
    
    def createRequest(self, name, **args):
        return { "name": name, "args" : args }
    
    async def send(self, json):
        self._conn.send(_json.dumps(json))
    
    async def initConnection(self):
        self._conn = _websocket.websocket("ws://" + self._host + self._port)

        logger = self.createRequest("mac", mac=self._addr)
        await self.send(logger)
        
        nameInfo = self.createRequest("setName", self._name)
        await self.send(nameInfo)
    
        typeInfo = self.createRequest("setType", self._type)
        await self.send(typeInfo)
    
    async def close(self):
        self._conn.close()
    
    async def main(self):
        await self.initConnection()
        while True:
            request = await self.recv()
            try:
                result = await self.LIST.execute(self, json.loads(request))
                self.send(result)
            except:
                pass
    
    async def recv(self):
        data = None
        while not data:
            data = self._conn.recv()
            try:
                data = _json.loads(data)
            except:
                pass
        return data

