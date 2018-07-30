import socket
import sys
import select
import utils

class ChatServer(object):
    
    def __init__(self, port):
        self.socket = socket.socket()
        self.socket.bind(("", int(port)))
        self.socket.listen(5)
        self.username_dict = {}
        self.channel_list = []
        self.channel_dict = {}
        self.socket_list = [self.socket]

    def send(self, socket, msg):
        socket.send(msg)

    def broadcast(self, channel, msg, socket):
        for sock in self.socket_list:
            if (sock != self.socket) and (sock != socket):
                if self.channel_dict.has_key(sock):
                    if self.channel_dict[sock] == channel:
                        self.send(sock, msg)

    def start(self):
        buf = ''
        while True:
            ready_to_read, ready_to_write, in_error = select.select(self.socket_list, [], [], 0)
            for socket in ready_to_read:
                if socket == self.socket:
                    (new_socket, address) = self.socket.accept()
                    self.socket_list.append(new_socket)
                else:
                    msg = socket.recv(utils.MESSAGE_LENGTH)
                    if not msg:
                        if self.channel_dict.has_key(socket):
                            channel_name = self.channel_dict[socket]
                            self.broadcast(channel_name, utils.SERVER_CLIENT_LEFT_CHANNEL.format(self.username_dict[socket]) + '\n', socket)
                            self.socket_list.remove(socket)
                            del self.username_dict[socket]
                            del self.channel_dict[socket]
                            socket.shutdown(1)
                    else:
                        buf += msg
                        if len(buf) >= utils.MESSAGE_LENGTH:
                            if not self.username_dict.has_key(socket):
                                self.username_dict[socket] = buf.rstrip()
                                buf = ''
                            else:
                                username = self.username_dict[socket]
                                if buf[0] == '/':
                                    control_msg = buf[1:]
                                    if control_msg.rstrip() == 'list':
                                        response = ""
                                        for channel in self.channel_list:
                                            response += channel
                                            response += '\n'
                                        self.send(socket, response)
                                        buf = ''
                                    elif control_msg[:4] == 'join':
                                        channel_name = control_msg[5:].rstrip()
                                        buf = ''
                                        if channel_name == '':
                                            response = utils.SERVER_JOIN_REQUIRES_ARGUMENT + '\n'
                                            self.send(socket, response)
                                        elif channel_name in self.channel_list:
                                            ignore = False
                                            if self.channel_dict.has_key(socket):
                                                old_channel_name = self.channel_dict[socket]
                                                if old_channel_name == channel_name:
                                                    ignore = True
                                                else:
                                                    self.broadcast(old_channel_name, utils.SERVER_CLIENT_LEFT_CHANNEL.format(username) + '\n', socket)
                                            if not ignore:
                                                self.channel_dict[socket] = channel_name
                                                self.broadcast(channel_name, utils.SERVER_CLIENT_JOINED_CHANNEL.format(username) + '\n', socket)
                                        else:
                                            response = utils.SERVER_NO_CHANNEL_EXISTS.format(channel_name) + '\n'
                                            self.send(socket, response)
                                    elif control_msg[:6] == 'create':
                                        channel_name = control_msg[7:].rstrip()
                                        buf = ''
                                        if channel_name == '':
                                            response = utils.SERVER_CREATE_REQUIRES_ARGUMENT + '\n'
                                            self.send(socket, response)
                                        elif channel_name in self.channel_list:
                                            response = utils.SERVER_CHANNEL_EXISTS.format(channel_name) + '\n'
                                            self.send(socket, response)
                                        else:
                                            if self.channel_dict.has_key(socket):
                                                old_channel_name = self.channel_dict[socket]
                                                self.broadcast(old_channel_name, utils.SERVER_CLIENT_LEFT_CHANNEL.format(username) + '\n', socket)
                                            self.channel_list.append(channel_name)
                                            self.channel_dict[socket] = channel_name
                                    else:
                                        response = utils.SERVER_INVALID_CONTROL_MESSAGE.format(buf.rstrip()) + '\n'
                                        self.send(socket, response)
                                        buf = ''
                                elif not self.channel_dict.has_key(socket):
                                    response = utils.SERVER_CLIENT_NOT_IN_CHANNEL + '\n'
                                    self.send(socket, response)
                                    buf = ''
                                else:
                                    channel = self.channel_dict[socket]
                                    broadcast_msg = '[' + username + '] ' + buf.rstrip() + '\n'
                                    self.broadcast(channel, broadcast_msg, socket)
                                    buf = ''
 
args = sys.argv
if len(args) != 2:
    print "Please supply a port."
    sys.exit()
server = ChatServer(args[1])
server.start()