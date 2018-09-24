from collections import namedtuple

StatusTuple = namedtuple("Status", ["InProgress","Done"])

class Request:
    """ Request """
    Status = StatusTuple(InProgress="In Progress", Done = "Done")

    def __init__(self, id, requester, status = Status.InProgress, states = None):
        #TODO: make this not changeable (id)
        self.request_id = id
        self.requester = requester
        self.status = status
        self.states = states if states else []
    
    def get_states(self):
        """ Return list of states """
        return self.states

    def get_last_state(self):
        if self.states:
           return self.states[len(self.states)-1]

    def push_state(self, state):
        self.states.append(state)

    def to_dico(self):
        dico = self.__dict__    
        dico['__request__'] = True
        return dico
 