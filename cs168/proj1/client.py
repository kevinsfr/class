import socket
import sys
import select
import utils

class ChatClient(object):

    def __init__(self, username, address, port):
        self.username = username
        self.address = address
        self.port = int(port)
        self.socket = socket.socket()
        try:
            self.socket.connect((self.address, self.port))
        except:
            sys.stdout.write(utils.CLIENT_WIPE_ME + '\r' + utils.CLIENT_CANNOT_CONNECT.format(self.address, self.port) + '\n')
            sys.exit()
        msg = username
        while len(msg) < utils.MESSAGE_LENGTH:
            msg += ' '
        self.send(msg)

    def send(self, message):        
        self.socket.send(message)

    def start(self):
        sys.stdout.write(utils.CLIENT_MESSAGE_PREFIX)
        sys.stdout.flush()
        while True:
            ready_to_read,ready_to_write,in_error = select.select([sys.stdin, self.socket], [], [])
            for socket in ready_to_read:             
                if socket == self.socket:
                    msg = socket.recv(utils.MESSAGE_LENGTH)
                    if not msg:
                        sys.stdout.write(utils.CLIENT_WIPE_ME + '\r' + utils.CLIENT_SERVER_DISCONNECTED.format(self.address, self.port) + '\n')
                        sys.exit()
                    else :
                        sys.stdout.write(utils.CLIENT_WIPE_ME + '\r' + msg)          
                else :
                    msg = raw_input()
                    while len(msg) < utils.MESSAGE_LENGTH:
                        msg += ' '
                    self.send(msg)
                sys.stdout.write(utils.CLIENT_MESSAGE_PREFIX)
                sys.stdout.flush()


args = sys.argv
if len(args) != 4:
    print "Please supply a username, server address and port."
    sys.exit()
client = ChatClient(args[1], args[2], args[3])
client.start()
