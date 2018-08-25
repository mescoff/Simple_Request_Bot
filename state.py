class State:

    def __init__(self, id, question, response = ""):
        self.state_id = id
        self.question = question
        self.response = response

    def to_dico(self, obj):
        dico = obj.__dico__
        dico['__state__'] = True
        return dico