import sys
from robot import *
import uasyncio as asyncio

def main(args):
    robot = MicroportalRobot("TheRobotName", "microportal.server.address", 8266)
    asyncio.run(robot.main())

if __name__ == "__main__" or True:
    main([])
