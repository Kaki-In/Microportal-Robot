from .action import *
from .physical import *

class RobotActionsList(ActionsList):
    def __init__(self):
        super().__init__()
        self._phy = PhysicalActionsList()
        self.addActionListener("executeAction", self.executeAction)
    
    async def executeAction(self, robot, actionName, args):
        return await self._phy.execute(robot, {"name":actionName, "args":args})

