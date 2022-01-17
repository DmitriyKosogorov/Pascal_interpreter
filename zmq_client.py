import zmq
import json

context = zmq.Context()

#  Socket to talk to server

print("choose mode of interpreting: 1-dict of VARs, 2- parsing tree")
mode = input()
if(mode in ['1','2']):
    print("Insert code here")
    program=input()
    print("Connecting to hello world server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    dict_message={'mode':mode, 'program':program}
    dict_message = json.dumps(dict_message)
    print("Sending request …")
    
    socket.send_string(dict_message)
    
    
    message = socket.recv()
    message=str(message.decode("utf-8"))
    print(f"Received reply: \n {message} ")
else:
    print('invalid mode')