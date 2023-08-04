import uasyncio as _asyncio
from uwebsockets import client as _websocket
import ujson as _json
import usocket as _socket
from .actions import *

class MicroportalConnection():
    LIST = RobotActionsList()
    
    def __init__(self, addr, name, host, port):
        self._conn = None
        self._addr = addr
        self._name = name
        self._host = host
        self._port = port
    
    def createRequest(self, requestName, **args):
        return { "name": requestName, "args" : args }
    
    async def send(self, json):
        self._conn.send(_json.dumps(json))
    
    async def initConnection(self):
        self._conn = _websocket.connect("ws://" + self._host + ":" + str(self._port) + "/robot")

        logger = self.createRequest("mac", mac=self._addr)
        await self.send(logger)
        
        nameInfo = self.createRequest("setRobotName", name=self._name)
        await self.send(nameInfo)
    
        typeInfo = self.createRequest("setRobotType", type="ESP8266")
        await self.send(typeInfo)
    
    async def close(self):
        if self._conn is not None:
            self._conn.close()
    
    async def main(self):
        await self.initConnection()
        while True:
            try:
                request = await self.recv()
            except _socket.timeout:
                pass
            result = await self.LIST.execute(self, request)
            await self.send(result)
    
    async def recv(self):
        data = None
        while not data:
            data = self._conn.recv()
            try:
                data = _json.loads(data)
            except:
                pass
        return data

