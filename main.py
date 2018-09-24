import json
import os.path
from components.request import Request
from components.state import State
from helper import helper

requests_file = "data/requests.json"

def run(input):
    parameters = json.loads(input)
    current_user = parameters["FromUser"]
    #avoid syntax error
    requester_message = parameters["Message"].strip()

    #verify requests file exists and isn't empty
    requests = helper.get_requests() if (os.path.isfile(requests_file) and os.stat(requests_file).st_size !=0) else []

    ## NEW REQUEST
    if "new request" in requester_message.lower():  

        #create request
        if requests:
            last_request = requests[len(requests)-1]
            request_id = last_request.request_id+1
        else:
            request_id = 0
        current_request = Request(request_id,current_user,Request.Status.InProgress)
        #TODO: replace response_id with state_id
        bot_reponse = helper.generate_response(None,"0",current_request, requests, "", is_new_request=True)
        return str.format("New bot request {0} started. {1}",current_request.request_id,bot_reponse)

    else:
        if not requests: return "No requests exist at the moment"
        
        current_request = requests.pop()
        #current_request_states = current_request.get_states()
        last_state = current_request.get_last_state()
        if not last_state: return str.format("I encountered an error. Request with id {0} has no states.", current_request.request_id)

        #query current state
        if requester_message in ["request state","status"]: 
            return str.format("Current request step: {0}",last_state.__dict__) #do a tostring with more info about state
        
        if current_user == current_request.requester:
            if last_state.question_id == "0":
                bot_reponse = helper.generate_response(last_state,"1",current_request,requests,requester_message)
                return bot_reponse
            elif last_state.question_id == "1":
                validation = helper.validate_message(last_state,requester_message)
                if False in validation: return validation[1]    

                bot_reponse = helper.generate_response(last_state,"2",current_request,requests,requester_message)
                return bot_reponse
            elif last_state.question_id == "2":
                validation = helper.validate_message(last_state,requester_message)
                if False in validation: return validation[1]

                bot_response = helper.generate_response(last_state,"3",current_request,requests,requester_message)
                #TODO: issue if conf msg fails. State is still added and we're at next step
                confirmation_msg = helper.generate_confirmation_script(current_request.get_states())
                return str.format("{0} \n {1}",bot_response, confirmation_msg)
            
            elif last_state.question_id == "3":
                #TODO: user helper validation here
                if requester_message.lower() in ["yes","y"]:
                    bot_response = helper.generate_response(last_state,"4",current_request,requests,requester_message)
                    #create IMPULSE requests
                    return bot_response
                elif requester_message.lower() in ["no","n"]:
                    return "Function needs to be implemented"
                else:
                    return "Your response did not match what we expected. Try again"
            else:
                return str.format("Hi {0}. We are processing your request. Will get back to you asap", current_user)
        else:
            return "A request process was already started. You are not the current requester. Discarding your message"            
