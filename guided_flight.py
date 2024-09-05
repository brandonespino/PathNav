from base64 import decode
import threading 
import socket
import collections
import cv2 as cv
import helpers

resp_address = ('', 9000) # receive tello responses
state_address = ('0.0.0.0', 8890) # receive tello states
vid_address = ('0.0.0.0', 11111) # recieve tello video
tello_address = ('192.168.10.1', 8889)

resp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
resp_sock.bind(resp_address)

state_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
state_sock.bind(state_address)

def recv():
    while True:
        try:
            resp_data, server = resp_sock.recvfrom(1518)
            print(resp_data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break
# def state_recv():
#     count = 0
#     while True: 
#         try:
#             if count%100 == 0:
#                 state_data, server = state_sock.recvfrom(1518)
#                 decoded_state_data = state_data.decode(encoding="utf-8")
#                 state_vals = helpers.state_formatter(decoded_state_data, True)  # receicing tuple of states to feed to database
#                 print(state_vals)
#                 helpers.sql_feed('localhost', 'brandon', 'brandon', 'Br@0nat9am', '5433', state_vals)
#                 print("returned from sql_feed")
#             count+=1
#         except Exception:
#             print ('\nState Exit . . .\n')
#             break

last_5_states = collections.deque(maxlen=5)
def state_recv():
    count = 0
    while True: 
        try:
            state_data, server = state_sock.recvfrom(1518)
            decoded_state_data = state_data.decode(encoding="utf-8")
            state_vals = helpers.state_formatter(decoded_state_data, True)
            last_5_states.append(state_vals)
            if count%50 == 0:
                print(state_vals)
            count+=1
        except Exception:
            print ('\nState Exit . . .\n')
            break

# idea is to input "frame" into network and after processing in cnn to an "edge dected" 
# image (hopefully with borders colored in) use opencv to draw my rectangle, 
# then assess how far drone position "p" is from left and right borders which will 
# be used in calculation of degree turn ccw or cw
def vid_recv():
    tello_video = cv.VideoCapture("udp://@0.0.0.0:11111")
    print('tello video connect')
    while True:
        try:
            retval, frame = tello_video.read() # retval is bool, frame is a cv matrix type
            print(retval)
            if retval:
                cv.namedWindow("live stream", 600)
                cv.imshow('live stream', frame)  # I can probably draw on the frame at some point to show the drone decisions
            if cv.waitKey(1) & 0xFF == ord("q"):
                break
        except Exception as err:
            print(err)
    tello_video.release()
    cv.destroyAllWindows()

print ('\r\n\r\nTello Python3 Demo.\r\n')
print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')
print ('       end -- quit demo.\r\n')

print('recv_thread')
recv_thread = threading.Thread(target=recv, name="recv thread", daemon=True)
recv_thread.start()
print('rcv_thread started')

print('state_recv_thread')
state_recv_thread = threading.Thread(target=state_recv, name="state thread", daemon=True)
state_recv_thread.start()
print('state_rcv_thread started')

print('vid_recv_thread')
vid_recv_thread = threading.Thread(target=vid_recv, name="vid thread", daemon=True)
vid_recv_thread.start()
print('vid_rcv_thread started')

# intialization & stream activation
msg = "command".encode(encoding="utf-8") 
sent = resp_sock.sendto(msg, tello_address)
print("command sent: {}".format(sent))

msg = "streamon".encode(encoding="utf-8") 
sent = resp_sock.sendto(msg, tello_address)
print("streamon sent: {}".format(sent))

while True: 
    try:
        msg = input("")
        if not msg:
            break
        if 'end' in msg:
            print ('...')
            sent = resp_sock.sendto("land".encode(encoding="utf-8"), tello_address)
            resp_sock.close()
            state_sock.close()
            print(last_5_states)
            break
        msg = msg.encode(encoding="utf-8") 
        sent = resp_sock.sendto(msg, tello_address)
    except KeyboardInterrupt:
        print ('\n . . .\n')
        resp_sock.close()
        state_sock.close()
        break