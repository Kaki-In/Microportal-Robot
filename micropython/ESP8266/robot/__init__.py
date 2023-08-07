from .wifi import *
from .microportal import *
import uasyncio as _asyncio

class MicroportalRobot():
    def __init__(self, name, host, port):
        self._wifi = WifiManager("ssid", "password")
        self._conn = None
        self._name = name
        self._host = host
        self._port = port
    
    async def initConnection(self):
        self._conn = MicroportalConnection(self._wifi.macAddress(), self._name, self._host, self._port)
        
    async def main(self):
        _asyncio.create_task(self._wifi.start())
        await self.run()
    
    async def run(self):
        while True:
            if not self._wifi.isConnected():
                print("Waiting for connection...")
                await self._wifi.waitForConnection()
                print("Connected")
            try:
                await self.initConnection()
                await self._conn.main()
            except Exception as exc:
                print("an error occured :", exc)
                await _asyncio.sleep(10)
            finally:
                await self._conn.close()
                print("disconnected")
