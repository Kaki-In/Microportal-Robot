class ActionsList():
    def __init__(self):
        self._actions = {}
        
    def addActionListener(self, action, func):
        self._actions[ action ] = func
    
    async def execute(self, robot, request):
        if type(request) is list:
            results = []
            for req in request:
                results.append(await self.execute(robot, req))
            return results
        try:
            name, args = request[ 'name' ], request[ 'args' ]
            return await self._actions[ name ] ( robot, **args )
        except Exception as exc:
            print("an exception occured :", repr(exc))
