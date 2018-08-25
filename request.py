from collections import namedtuple

StatusTuple = namedtuple("Status", ["InProgress","Done"])
Status = StatusTuple(InProgress="In Progress", Done = "Done")

class Request:

    def __init__(self, id, user, status, states = None):
        self.request_id = id
        self.user = user
        self.status = status
        self.states = states if states else []
    
    def get_states(self):
        return self.states

    def get_last_state(self):
        return self.states.pop()

    def to_dico(self,obj):
        dico = obj.__dico__
        dico['__request__'] = True
        return dico
 