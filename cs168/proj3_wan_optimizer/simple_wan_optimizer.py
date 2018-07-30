import wan_optimizer
import utils
import tcp_packet

class WanOptimizer(wan_optimizer.BaseWanOptimizer):
    """ WAN Optimizer that divides data into fixed-size blocks.

    This WAN optimizer should implement part 1 of project 4.
    """

    # Size of blocks to store, and send only the hash when the block has been
    # sent previously
    BLOCK_SIZE = 8000

    def __init__(self):
        wan_optimizer.BaseWanOptimizer.__init__(self)
        # Add any code that you like here (but do not add any constructor arguments).
        self.hash_table = {}
        self.buffers = {}
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

    def send_block_wan(self, pair, is_fin):
        additional = False
        if len(self.buffers[pair]) > self.BLOCK_SIZE:
            block = self.buffers[pair][:self.BLOCK_SIZE]
            self.buffers[pair] = self.buffers[pair][self.BLOCK_SIZE:]
            if is_fin:
                additional = True
        else:
            block = self.buffers[pair]
            self.buffers[pair] = ""
        if block not in self.hash_table.keys():
            self.hash_table[block] = utils.get_hash(block)
            if not additional:
                self.send_raw_data(pair, block, is_fin, self.wan_port)
            else:
                self.send_raw_data(pair, block, False, self.wan_port)
        else:
            self.send_hash(pair, self.hash_table[block], is_fin)
        if additional:
            self.send_block_wan(pair, True)

    def send_block_local(self, pair, is_fin, port):
        block = self.buffers[pair]
        self.buffers[pair] = ""
        if block not in self.hash_table.keys():
            self.hash_table[block] = utils.get_hash(block)
        self.send_raw_data(pair, block, is_fin, port)

    def receive(self, packet):
        """ Handles receiving a packet.

        Right now, this function simply forwards packets to clients (if a packet
        is destined to one of the directly connected clients), or otherwise sends
        packets across the WAN. You should change this function to implement the
        functionality described in part 1.  You are welcome to implement private
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
                else:
                    self.buffers[pair] += payload
                if packet.is_fin:
                    self.send_block_local(pair, True, self.address_to_port[packet.dest])
                else:
                    if len(self.buffers[pair]) >= self.BLOCK_SIZE:
                        self.send_block_local(pair, False, self.address_to_port[packet.dest])
        else:
            # The packet must be destined to a host connected to the other middlebox
            # so send it across the WAN.
            if pair not in self.buffers.keys():
                self.buffers[pair] = payload
            else:
                self.buffers[pair] += payload
            if packet.is_fin:
                self.send_block_wan(pair, True)
            else:
                if len(self.buffers[pair]) >= self.BLOCK_SIZE:
                    self.send_block_wan(pair, False)

