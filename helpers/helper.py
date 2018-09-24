import json
import os
import helpers.json_handlers as jhandler
from components.request import Request
from components.state import State


#TODO: requests file per user
#in Main make switch easier for response

#possible bug here with requests file path depending on where original script is started from
requests_file = 'data/requests.json'

script_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(script_path,'response_list.json'),'r') as f:
    bot_response_dico = json.load(f)
with open(os.path.join(script_path,'primaryCl.json'),'r') as f:
    primary_CL_dico = json.load(f)
with open(os.path.join(script_path,'priorities.json'),'r') as f:
    priorities_dico = json.load(f)

def generate_response(last_state, bot_response_id, current_request, requests, requester_response, is_new_request=False):
    """Generate a response absed on current input. Will save response inside current request"""
    state_id = 0 if not last_state else (last_state.state_id+1)
    #TODO: bot_response_id = state_id ?
    current_state = State(state_id, bot_response_id, requester_response)
    current_request.push_state(current_state)
    #Repush request on stack and save to file
    requests.append(current_request)
    with open(requests_file,'w') as outfile:
        json.dump(requests,outfile,cls=jhandler.ComplexHandler,indent=4)
    return bot_response_dico[bot_response_id]


def validate_message(last_state,requester_message):
    """ Return array [<boolean>,<message if unvalid resp>]"""
    invalid_resp_msg = str.format("Your response <{0}> is not in the right format. Try again\n{1}",requester_message,bot_response_dico[last_state.question_id])
    invalid_resp_result = [False,invalid_resp_msg]

    if last_state.question_id == "1":
        if requester_message.strip() not in primary_CL_dico.keys():
            return invalid_resp_result
    elif last_state.question_id == "2":
        if requester_message.strip() not in priorities_dico.keys():
            return invalid_resp_result
    return [True]

def get_requests():
    """Return list of requests [{request1},{request2}]"""
    try:
        with open(requests_file,"r") as f:
            requests = json.load(f, object_hook=jhandler.obj_decoder)
            return requests
    except TypeError as err:
        print(err)
        return None

def generate_confirmation_script(states):
    attributes = ["NA","Summary","Primary CL","Impact"]
    if len(states) == 4:
        i = 1
        resp_list=[]
        while (i < len(states)):
            resp_list.append(str.format(" {0}:{1}.",attributes[i],states[i].response.strip()))
            i+=1
        return ''.join(resp_list)
    else:
        return str.format("Error. Request has {0} states, but we are expecting 4", len(states))    
   
