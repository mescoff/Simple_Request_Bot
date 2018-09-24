import json
from components.request import Request
from components.state import State

class ComplexHandler(json.JSONEncoder):
    #pylint: disable=E0202
    def default(self,obj):
        if hasattr(obj,'to_dico'):
            return obj.to_dico()
        return json.JSONEncoder.default(self, obj)

def obj_decoder(dico):
    if '__request__' in dico: 
        return Request(dico['request_id'], dico['requester'], dico['status'], dico['states'])
    if '__state__' in dico:
        return State(dico['state_id'], dico['question_id'], dico['response']) 
    return dico    