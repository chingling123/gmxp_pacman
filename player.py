from actions import Actions

class Player:
    token = ""
    actions = []

    def __init__(self, *args, **kwargs):
        act = Actions()
        act.code = "PARTICIPATION"
        act.amount = 1
        self.actions = []
        self.actions.append(act)

    def addAction(self, code, amount):
        act = Actions()
        act.code = code
        act.amount = amount
        self.actions.append(act)
    
    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)