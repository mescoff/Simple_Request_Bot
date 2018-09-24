import sys
import json
import main 
from components.request import Request
from components.state import State
from helper import helper

def test1():
    arg = ' '.join(e for e in sys.argv[1:])
    message = json.dumps({"FromUser":"manon.escoffier@sgcib.com","Message":arg})
    print(main.run(message))

def test2():
    req1 = Request("0","me")
    req2 = Request("1","Sonia")
    state1 = State("0","Describe your issue")
    state2 = State("1","What application is it for","I need this")
    req1.push_state(state1)
    req2.push_state(state2)
    requests = []
    requests.append(req1)
    requests.append(req2)

    with open("test.json","w") as f :
        json.dump(requests,f,cls=helper.ComplexHandler, indent=4)
    with open("test.json","r") as f :
        l = json.load(f, object_hook=helper.obj_decoder)
    print(type((l[0].states)[0]))

def test3(arg):
    message = json.dumps({"FromUser":"manon.escoffier@sgcib.com","Message":arg})
    print(main.run(message))

if __name__ == "__main__":

    test1()
    #test3("New request")
    #test3("somethg")
    #test3("1")

