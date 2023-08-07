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
        
        self._pongged = True
    
    def createRequest(self, requestName, **args):
        return { "name": requestName, "args" : args }

    def setPongged(self):
        print("The server pongged")
        self._pongged = True
    
    async def send(self, json):
        self._conn.send(_json.dumps(json))
    
    async def initConnection(self):
        self._conn = _websocket.connect("ws://" + self._host + ":" + str(self._port) + "/robot")
        print("Connected")
        
        self._conn.settimeout(0.5)
        
        logger = self.createRequest("mac", mac=self._addr)
        await self.send(logger)
        
        nameInfo = self.createRequest("setRobotName", name=self._name)
        await self.send(nameInfo)
    
        typeInfo = self.createRequest("setRobotType", type="ESP8266")
        await self.send(typeInfo)
    
    async def close(self):
        if self._conn is not None:
            try:
                self._conn.close()
            except OSError:
                pass
    
    async def _pingEveryTime(self):
        while self._pongged:
            print("Pinging the server...")
            await self.send(self.createRequest("__ping__"))
            self._pongged = False
            await _asyncio.sleep(10)
        print("The server didn't pong, exiting...")
        await self.close()
    
    async def main(self):
        await self.initConnection()
        _asyncio.create_task(self._pingEveryTime())
        while True:
            request = await self.recv()
            result = await self.LIST.execute(self, request)
            if result is not None:
                await self.send(result)
    
    async def recv(self):
        data = None
        while not data:
            try:
                data = self._conn.recv()
            except OSError as oserr:
                if oserr.errno != 110 : # 110 = timeout
                    raise
                await _asyncio.sleep(1)
                continue
            data = _json.loads(data)
        return data

