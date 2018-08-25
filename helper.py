import json
from request import Request
from state import State

class ComplexEncoder(json.JSONEncoder):
    #pylint: disable=E0202
    def default(self,obj):
        if hasattr(obj,'to_dico'):
            return obj.to_dico()
        return json.JSONEncoder.default(self, obj)

def obj_encode(dico):
    if '__request__' in dico: 
        return Request(dico['request_id'], dico['user'], dico['status'], dico['states'])
    if '__state__' in dico:
        return State(dico['state_id'], dico['question'], dico['response'])
