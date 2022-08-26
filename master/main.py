import socket
import time
import threading
import time
from djitellopy import Tello

tello = None

takeoff = False
land = True

# connect tello
while True:
    if tello is not None:
        break
    try:
        tello = Tello()
        tello.connect()
    except Exception:
        print(Exception)
        print("Connection Failure, trying again.. ")
        time.sleep(5)
    
# socket init
HOST = '192.168.0.101'
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

_socket = True
command = None


# tello 
SPEED = 40
s = None
data = None

def makeSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while _socket:
        conn, addr = s.accept()    
        global command
        global data
        try:
            # with conn:
            data = f"command,{command}"
            conn.sendall(bytes(data,"utf-8"))
            if command is not None and command.split(",")[0] in ["flip"]:
                command = f"move,0,0,0,0"
        except Exception as e:
            print(e)
            conn.close()

def telloControl():
    while True:
        global takeoff
        global land
        global command
        data = f"command,{command}"
        if data != "" and data is not None:
            _split = data.split(",")
            if _split[1] !="None":
                try:
                    if _split[1] == "takeoff" and takeoff == False:
                        print('Received', _split)
                        print("Taking off")
                        tello.takeoff()
                        takeoff = True
                        land = False
                    if _split[1] == "land" and land == False:
                        print('Received', data)
                        print("Landing")
                        tello.land()
                        takeoff = False
                        land = True

                    if _split[1] == "rotate_left":
                        print('Received', data)
                        print("Rotating left")
                        tello.rotate_clockwise(360)
                        
                    if _split[1] == "rotate_right":
                        print('Received', data)
                        print("Rotating left")
                        action = tello.rotate_counter_clockwise(360)
                        print(action)
                    
                    if _split[1] == "stop":
                        print('Received', data)
                        _move = (0,0,0,0)
                        print("Stopping", _move)
                        tello.send_rc_control(int(_move[0]),int( _move[1]), int(_move[2]), int(_move[3]))

                    if _split[1] == "move" and takeoff == True:
                        print('Received', data)
                        _move = (_split[2], _split[3], _split[4], _split[5])
                        print("Moving", _move)
                        tello.send_rc_control(int(_move[0]),int( _move[1]), int(_move[2]), int(_move[3]))

                    if _split[1] == "flip" and takeoff == True:
                        print('Received', data)
                        tello.flip(_split[2])

                    if _split[1] == "quit":
                        break
                except Exception as e:
                    print(e)

socket_thread = threading.Thread(target=makeSocket).start()
tello_thread = threading.Thread(target=telloControl).start()

while True:
    _cmd = input("Enter commands: ")
    _cmd = _cmd.lower()
    print(_cmd)
    try:
        if _cmd == "takeoff":
            command = "takeoff"
        elif _cmd == "land":
            command = "land"
        elif _cmd == "stop":
            command = "stop"
        elif _cmd == "move_forward":
            # left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
            command = f"move,0,{SPEED},0,0"
        
        elif _cmd == "move_backward":
            # left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
            command = f"move,0,{-SPEED},0,0"
        
        elif _cmd == "move_up":
            # left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
            command = f"move,0,0,{SPEED},0"
        
        elif _cmd == "move_down":
            # left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
            command = f"move,0,0,{-SPEED},0"

        elif _cmd == "move_left":
            # left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
            command = f"move,{SPEED},0,0,0"
        
        elif _cmd == "move_right":
            # left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
            command = f"move,{-SPEED},0,0,0"

        elif _cmd == "rotate_left":
            # left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
            command = f"rotate_left"
        elif _cmd == "rotate_right":
            # left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
            command = f"rotate_right"
        
        elif _cmd == "flip_right":
            command = f"flip,r"
            if takeoff == True:
                tello.flip('r')
            
        elif _cmd == "flip_left":
            command = f"flip,l"
            if takeoff == True:
                tello.flip('l')
            
        elif _cmd == "flip_forward":
            command = f"flip,f"
            if takeoff == True:
                tello.flip('f')
            
        elif _cmd == "flip_backward":
            command = f"flip,b"
            if takeoff == True:
                tello.flip('b')
        elif _cmd == "exit":
            command = None
            _socket = False
            command = "quit"
            break
        else:
            print("Command not found")
    except  Exception as e:
        print(e)
    time.sleep(0.4)

if tello is not None:
    tello.end()
if s is not None:
    s.close()
socket_thread.end()