from .action import *
from .physical import *

class RobotActionsList(ActionsList):
    def __init__(self):
        super().__init__()
        self._phy = PhysicalRobotsList()
        self.addActionListener("executeAction", self.executeAction)
    
    async def executeAction(self, robot, name, args):
        return await self._phy.execute(robot, {"name":name, "args":args})

