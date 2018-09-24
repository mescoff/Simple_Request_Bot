import json
with open('helpers/response_list.json', 'r') as f:
    bot_response_dico = json.load(f)

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
        return str.format("- StateId: {0}\n- Question asked: {1}\n- Your response: {2}", self.state_id, bot_response_dico[self.question_id], self.response)