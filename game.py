
import json
import uuid

class Game:
    partnerId = ""
    startTime = 0
    finishTime = 0
    players = []

    def __init__(self, *args, **kwargs):
        self.players = []
        self.partnerId = "FC-" + str(uuid.uuid4())

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)