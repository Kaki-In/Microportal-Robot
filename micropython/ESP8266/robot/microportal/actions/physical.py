from .action import *
import machine as _machine
import uasyncio as _asyncio

class PhysicalActionsList(ActionsList):
    def __init__(self):
        super().__init__()

        self.addActionListener("setPin", self.setPin)
        self.addActionListener("getpin", self.getPin)
        self.addActionListener("getPinPullUp", self.getPinPullUp)
        self.addActionListener("sleep", self.sleep)
    
    async def setPin(self, robot, pin, active):
        pin = _machine.Pin(pin, _machine.Pin.OUT)
        if active:
            pin.on()
        else:
            pin.off()

    async def getPin(self, robot, pin):
        pin = _machine.Pin(pin, _machine.Pin.IN)
        return robot.createRequest("getPinResult", pin=pin, active=pin.active())

    async def getPinPullUp(self, robot, pin):
        pin = _machine.Pin(pin, _machine.Pin.PULL_UP)
        return robot.createRequest("getPinResult", pin=pin, active=pin.active())
    
    async def sleep(self, robot, time):
        await _asyncio.sleep(time)
