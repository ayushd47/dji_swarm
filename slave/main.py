#!/usr/bin/env python3
import socket
from djitellopy import Tello
import time

HOST = '192.168.0.101'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
takeoff = False
land = True
tello_connection = False
tello = None

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
    
# left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
        data = data.decode("utf-8")
        if data != "":
            _split = data.split(",")
            if _split[1] !="None":
                try:
                    if _split[1] == "takeoff" and takeoff == False:
                        print('Received', data)
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

                    if _split[1] == "rotate_left" and takeoff == True:
                        print('Received', data)
                        print("Rotating left")
                        tello.rotate_clockwise(360)
                        
                    if _split[1] == "rotate_right" and takeoff == True:
                        print('Received', data)
                        print("Rotating left")
                        tello.rotate_counter_clockwise(360)
                    
                    if _split[1] == "stop" and takeoff == True:
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
