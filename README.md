# DJI TELLO STANDARD SWARM Implementation

Since, DJI Standard has not been updated to SDK2.0, the access point cannot be changed. But, it can be done with multiple host connecting to tello individually and all host connected to a single network.

This process is tested with one Windows machine and 2 raspberry pi, all connecting to each tello. And each devices connected to a switch via ethernet. 

Although it is harder to manage, it is possible.

## Instruction
1. First connect all the devices to a switch, or a singular network. Ethernet(recommended)
2. Connect all the tello with each devices
3. Update the HOST ip in both master's and slave's main.py. : switch/ethernet ip address of the machine where ./master/main.py is running.
3. Run the master server  ./master/main.py
4. Run the slave client(s) ./slave/main.py
5. Type the commands in server

### Commands
1. takeoff
2. land
3. move_forward
4. move_backward
5. move_left
6. move_right
7. move_up
8. move_down
9. stop
10. rotate_left
11. rotate_right
12. flip_left
13. flip_right
14. flip_forward
15. flip_backward

## NOTE
### This source is still in alpha phase, can cause issues according to devices and tello.
