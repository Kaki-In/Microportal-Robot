from .wifi import *
from .microportal import *
import uasyncio as _asyncio

class MicroportalRobot():
    def __init__(self, name, host, port):
        self._wifi = WifiManager()
        self._conn = None
        self._name = name
        self._host = host
        self._port = port
    
    async def initConnection(self)
        self._conn = MicroportalConnection(self._wifi.macAddress(), self._name, self._host, self._port)
        
    async def main(self):
        self._wifi.start()
        await self.run()
    
    async def run(self):
        while True:
            if not self._wifi.isConnected():
                await self._wifi.waitForConnection()
            self.initConnection()
            try:
                await self._conn.main()
            except Excpetion as exc:
                print("ann error occured :", err)
            finally:
                await self._conn.close()
