import network as _net
import uasyncio as _asyncio
import machine as _machine

class WifiManager():
    def __init__(self, ssid, password=None):
        self._ssid = ssid
        self._password = password
        self._wlan = _net.WLAN(_net.STA_IF)
        self._isRunning = False
        
        self._led = Pin(2, _machine.Pin.OUT)
        self._led.on()
    
    async def stop(self):
        self._isRunning = None
        while self._isRunning is None:
            _asyncio.sleep(0.1)
        
    async def start(self):
        self._isRunning = True
        while self._isRunning():
            if self.isConnected():
                await _asyncio.sleep(60)
                continue
            connStatus = self._wlan.status()
            if   connStatus is _net.STAT_CONNECTING:
                await self.displayConnectingLedAnimation()
            elif connStatus in ( _net.STAT_WRONG_PASSWORD, _net.STAT_NO_AP_FOUND, _net.STAT_CONNECT_FAIL ):
                await self._displayErrorLedAnimation()
                self.connect()
            else:
                self.connect()
        self._isRunning = False
   
   async def displayConnectingLedAnimation(self):
       self._led.off()
       await _asyncio.sleep(0.5)
       self._led.on()
       await _asyncio.sleep(0.5)
   
   async def waitForConnection(self):
       while not self.isConnected():
           _asyncio.sleep(30)

   async def displayErrorLedAnimation(self):
       for i in range(2):
           self._led.off()
           await _asyncio.sleep(0.1)
           self._led.on()
           await _asyncio.sleep(0.1)
       await _asyncio.sleep(1)
   
   def connect(self):
       if self._password is None:
           self._wlan.connect(self._ssid)
       else:
           self._wlan.connect(self._ssid, self._password)
   
   def isConnected(self):
       return self._wlan.isConnected()
   
   def macAddress(self):
       addr = list(self._wlan.config("mac"))
       mac = ""
       for i in addr:
           if mac :
               mac += ':'
           hex = hex(i)[ 2 : ]
           if len(hex) == 1:
               hex = "0" + hex
           mac += hex
       return mac
   
   def setSSID(self, ssid, password=None):
       self._ssid, self._password = ssid, password
       self._connect()
   

