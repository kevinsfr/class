import wan_optimizer
import utils
import tcp_packet

class WanOptimizer(wan_optimizer.BaseWanOptimizer):
    """ WAN Optimizer that divides data into variable-sized
    blocks based on the contents of the file.

    This WAN optimizer should implement part 2 of project 4.
    """

    # The string of bits to compare the lower order 13 bits of hash to
    GLOBAL_MATCH_BITSTRING = '0111011001010'
    WINDOW_SIZE = 48
    LAST_BITS_LENGTH = 13

    def __init__(self):
        wan_optimizer.BaseWanOptimizer.__init__(self)
        # Add any code that you like here (but do not add any constructor arguments).
        self.hash_table = {}
        self.buffers = {}
        self.window_start = {}
        return

    def send_raw_data(self, pair, block, is_fin, port):
        size = utils.MAX_PACKET_SIZE
        while size < len(block):
            payload = block[:size]
            block = block[size:]
            packet = tcp_packet.Packet(pair[0], pair[1], True, False, payload)
            self.send(packet, port)
        packet = tcp_packet.Packet(pair[0], pair[1], True, is_fin, block)
        self.send(packet, port)

    def send_hash(self, pair, hash_value, is_fin):
        packet = tcp_packet.Packet(pair[0], pair[1], False, is_fin, hash_value)
        self.send(packet, self.wan_port)

    def send_block_wan(self, pair, block, is_fin):
        if block not in self.hash_table.keys():
            self.hash_table[block] = utils.get_hash(block)
            self.send_raw_data(pair, block, is_fin, self.wan_port)
        else:
            self.send_hash(pair, self.hash_table[block], is_fin)

    def receive(self, packet):
        """ Handles receiving a packet.

        Right now, this function simply forwards packets to clients (if a packet
        is destined to one of the directly connected clients), or otherwise sends
        packets across the WAN. You should change this function to implement the
        functionality described in part 2.  You are welcome to implement private
        helper fuctions that you call here. You should *not* be calling any functions
        or directly accessing any variables in the other middlebox on the other side of 
        the WAN; this WAN optimizer should operate based only on its own local state
        and packets that have been received.
        """
        pair = (packet.src, packet.dest)
        payload = packet.payload
        if packet.dest in self.address_to_port:
            # The packet is destined to one of the clients connected to this middlebox;
            # send the packet there.
            if not packet.is_raw_data:
                for raw_data in self.hash_table.keys():
                    if self.hash_table[raw_data] == payload:
                        block = raw_data
                        self.send_raw_data(pair, block, packet.is_fin, self.address_to_port[packet.dest])
                        break
            else:
                if pair not in self.buffers.keys():
                    self.buffers[pair] = payload
                    self.window_start[pair] = 0
                else:
                    self.buffers[pair] += payload
                if len(self.buffers[pair]) >= self.WINDOW_SIZE:
                    match_found = True
                    while match_found and len(self.buffers[pair]) >= self.WINDOW_SIZE:
                        window = self.buffers[pair][self.window_start[pair]:self.window_start[pair] + self.WINDOW_SIZE]
                        last_bits = utils.get_last_n_bits(utils.get_hash(window), self.LAST_BITS_LENGTH)
                        while last_bits != self.GLOBAL_MATCH_BITSTRING:
                            self.window_start[pair] += 1
                            if self.window_start[pair] + self.WINDOW_SIZE > len(self.buffers[pair]):
                                match_found = False
                                break
                            window = self.buffers[pair][self.window_start[pair]:self.window_start[pair] + self.WINDOW_SIZE]
                            last_bits = utils.get_last_n_bits(utils.get_hash(window), self.LAST_BITS_LENGTH)
                        if match_found:
                            block = self.buffers[pair][:self.window_start[pair] + self.WINDOW_SIZE]
                            self.hash_table[block] = utils.get_hash(block)
                            is_fin = False
                            if self.window_start[pair] + self.WINDOW_SIZE == len(self.buffers[pair]):
                                if packet.is_fin:
                                    is_fin = True
                            self.send_raw_data(pair, block, is_fin, self.address_to_port[packet.dest])
                            if self.window_start[pair] + self.WINDOW_SIZE == len(self.buffers[pair]):
                                self.buffers[pair] = ""
                            else:
                                self.buffers[pair] = self.buffers[pair][self.window_start[pair] + self.WINDOW_SIZE:]
                            self.window_start[pair] = 0
                if packet.is_fin:
                    self.hash_table[self.buffers[pair]] = utils.get_hash(self.buffers[pair])
                    self.send_raw_data(pair, self.buffers[pair], True, self.address_to_port[packet.dest])
                    self.buffers[pair] = ""
                    self.window_start[pair] = 0
        else:
            # The packet must be destined to a host connected to the other middlebox
            # so send it across the WAN.
            if pair not in self.buffers.keys():
                self.buffers[pair] = payload
                self.window_start[pair] = 0
            else:
                self.buffers[pair] += payload
            if len(self.buffers[pair]) >= self.WINDOW_SIZE:
                match_found = True
                while match_found and len(self.buffers[pair]) >= self.WINDOW_SIZE:
                    window = self.buffers[pair][self.window_start[pair]:self.window_start[pair] + self.WINDOW_SIZE]
                    last_bits = utils.get_last_n_bits(utils.get_hash(window), self.LAST_BITS_LENGTH)
                    while last_bits != self.GLOBAL_MATCH_BITSTRING:
                        self.window_start[pair] += 1
                        if self.window_start[pair] + self.WINDOW_SIZE > len(self.buffers[pair]):
                            match_found = False
                            break
                        window = self.buffers[pair][self.window_start[pair]:self.window_start[pair] + self.WINDOW_SIZE]
                        last_bits = utils.get_last_n_bits(utils.get_hash(window), self.LAST_BITS_LENGTH)
                    if match_found:
                        block = self.buffers[pair][:self.window_start[pair] + self.WINDOW_SIZE]
                        is_fin = False
                        if self.window_start[pair] + self.WINDOW_SIZE == len(self.buffers[pair]):
                            if packet.is_fin:
                                is_fin = True
                        self.send_block_wan(pair, block, is_fin)
                        if self.window_start[pair] + self.WINDOW_SIZE == len(self.buffers[pair]):
                            self.buffers[pair] = ""
                        else:
                            self.buffers[pair] = self.buffers[pair][self.window_start[pair] + self.WINDOW_SIZE:]
                        self.window_start[pair] = 0
            if packet.is_fin:
                self.send_block_wan(pair, self.buffers[pair], True)
                self.buffers[pair] = ""
                self.window_start[pair] = 0
