import network as _net
import uasyncio as _asyncio
import machine as _machine

class WifiManager():
    def __init__(self, ssid, password=None):
        self._ssid = ssid
        self._password = password
        self._wlan = _net.WLAN(_net.STA_IF)
        self._isRunning = False

        self.connectToNetwork()
        
        self._led = _machine.Pin(2, _machine.Pin.OUT)
        self._led.on()
    
    async def stop(self):
        self._isRunning = None
        while self._isRunning is None:
            _asyncio.sleep(0.1)
        
    async def start(self):
        self._isRunning = True
        last = None
        while self._isRunning:
            if self.isConnected():
                if last is not _net.STAT_GOT_IP:
                    await self.displayConnectedLedAnimation()
                await _asyncio.sleep(60)
                last = _net.STAT_GOT_IP
                continue
            connStatus = self._wlan.status()
            if   connStatus is _net.STAT_CONNECTING:
                await self.displayConnectingLedAnimation()
            elif connStatus in ( _net.STAT_WRONG_PASSWORD, _net.STAT_NO_AP_FOUND, _net.STAT_CONNECT_FAIL ):
                print("An error occured...", connStatus)
                await self.displayErrorLedAnimation()
            else:
                self.connectToNetwork()
            last = connStatus
        self._isRunning = False
   

    async def displayConnectedLedAnimation(self):
        self._led.off()
        await _asyncio.sleep(1)
        self._led.on()
        await _asyncio.sleep(1)

    async def displayConnectingLedAnimation(self):
        self._led.off()
        await _asyncio.sleep(0.5)
        self._led.on()
        await _asyncio.sleep(0.5)
   
    async def waitForConnection(self):
        while not self.isConnected():
            await _asyncio.sleep(10)

    async def displayErrorLedAnimation(self):
        for i in range(2):
            self._led.off()
            await _asyncio.sleep(0.1)
            self._led.on()
            await _asyncio.sleep(0.1)
        await _asyncio.sleep(1)
   
    def connectToNetwork(self):
        if self._password is None:
            self._wlan.connect(self._ssid)
        else:
            self._wlan.connect(self._ssid, self._password)
   
    def isConnected(self):
        return self._wlan.isconnected()
   
    def macAddress(self):
        addr = list(self._wlan.config("mac"))
        mac = ""
        for i in addr:
            if mac :
                mac += ':'
            h = hex(i)[ 2 : ]
            if len(h) == 1:
                h = "0" + h
            mac += h
        return mac
   
    def setSSID(self, ssid, password=None):
        self._ssid, self._password = ssid, password
        self.connectToNetwork()
   
