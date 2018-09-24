class State:
    """ State """

    def __init__(self, id, question_id, response = ""):
        self.state_id = id
        self.question_id = question_id
        self.response = response

    def to_dico(self):
        dico = self.__dict__    
        dico['__state__'] = True
        return dico
    
    def to_string(self):
        pass