from interpreter import Interpreter
import json
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print('connecting')
message = socket.recv()
message=str(message.decode("utf-8"))
dict_message=json.loads(message)
if(dict_message['mode'] and dict_message['program']):
    print('message is goten')
    mode=dict_message['mode']
    program=dict_message['program']
    print(program)
    interpreter=Interpreter()
    if(mode=='1'):
        try:
            result = interpreter.interpret(program, mode)
            result = json.dumps(result)
        except Exception as e:
            result = str(e)
    if(mode=='2'):
        try:
            result = interpreter.interpret(program, mode)
            result=str(result)            
            result = json.dumps(result)
        except Exception as e:
            result = str(e)
    
    socket.send_string(result)
    print('result is sent')
else:
    print('invalid message was')
   