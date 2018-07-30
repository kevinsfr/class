"""Your awesome Distance Vector router for CS 168."""

import sim.api as api
import sim.basics as basics

# We define infinity as a distance of 16.
INFINITY = 16


class DVRouter(basics.DVRouterBase):
    # NO_LOG = True # Set to True on an instance to disable its logging
    POISON_MODE = True # Can override POISON_MODE here
    # DEFAULT_TIMER_INTERVAL = 5 # Can override this yourself for testing

    def __init__(self):
        """
        Called when the instance is initialized.

        You probably want to do some additional initialization here.

        """
        self.start_timer()  # Starts calling handle_timer() at correct rate
        self.dv = {}
        self.dv[self] = 0
        self.ports_latency = {}
        self.neighbors = {}
        self.direct_paths = {}
        self.paths = {}

    def handle_link_up(self, port, latency):
        """
        Called by the framework when a link attached to this Entity goes up.

        The port attached to the link and the link latency are passed
        in.

        """
        self.ports_latency[port] = latency
        for dst in self.dv.keys():
            self.send(basics.RoutePacket(dst, self.dv[dst]), port)


    def handle_link_down(self, port):
        """
        Called by the framework when a link attached to this Entity does down.

        The port number used by the link is passed in.

        """
        del self.neighbors[port]
        del self.ports_latency[port]
        for dst in self.paths.keys():
            if self.paths[dst][0] == port:
                del self.paths[dst]
                if not self.POISON_MODE:
                    del self.dv[dst]
                else:
                    self.dv[dst] = INFINITY
        for dst in self.direct_paths.keys():
            if self.direct_paths[dst] == port:
                del self.direct_paths[dst]
                if not self.POISON_MODE:
                    del self.dv[dst]
                else:
                    self.dv[dst] = INFINITY
        for neighbor in self.neighbors.keys():
            for dst in self.dv.keys():
                if self.paths.has_key(dst):
                    if self.paths[dst][0] == neighbor:
                        continue
                self.send(basics.RoutePacket(dst, self.dv[dst]), neighbor)

    def handle_rx(self, packet, port):
        """
        Called by the framework when this Entity receives a packet.

        packet is a Packet (or subclass).
        port is the port number it arrived on.

        You definitely want to fill this in.

        """
        #self.log("RX %s on %s (%s)", packet, port, api.current_time())
        if isinstance(packet, basics.RoutePacket):
            router = packet.src
            dst = packet.destination
            latency = packet.latency
            self.neighbors[port] = router
            if not self.dv.has_key(router):
                self.dv[router] = self.ports_latency[port]
                self.paths[router] = (port, api.current_time())
            if dst == self:
                return
            if latency == INFINITY:
                if self.paths.has_key(dst) and (self.paths[dst][0] == port):
                    del self.paths[dst]
                    self.dv[dst] = INFINITY
            if (not self.dv.has_key(dst)) or (self.dv[router] + latency <= self.dv[dst]):
                self.dv[dst] = self.dv[router] + latency
                self.paths[dst] = (port, api.current_time())
            
        elif isinstance(packet, basics.HostDiscoveryPacket):
            host = packet.src
            if self.dv.has_key(host):
                self.dv[host] = min(self.dv[host], self.ports_latency[port])
            else:
                self.dv[host] = self.ports_latency[port]
            self.direct_paths[host] = port
        else:
            # Totally wrong behavior for the sake of demonstration only: send
            # the packet back to where it came from!
            dst = packet.dst
            if not self.dv.has_key(dst) or self.dv[dst] == INFINITY:
                return
            if self.paths.has_key(dst):
                if port != self.paths[dst][0]:
                    self.send(packet, self.paths[dst][0])
                    return
            if self.direct_paths.has_key(dst):
                if port != self.direct_paths[dst]:
                    self.send(packet, self.direct_paths[dst])

    def handle_timer(self):
        """
        Called periodically.

        When called, your router should send tables to neighbors.  It
        also might not be a bad place to check for whether any entries
        have expired.

        """
        for dst in self.paths.keys():
            if (api.current_time() - self.paths[dst][1]) >= self.ROUTE_TIMEOUT:
                del self.paths[dst]
                if not self.direct_paths.has_key(dst):
                    del self.dv[dst]
                else:
                    self.dv[dst] = self.ports_latency[self.direct_paths[dst]]
        for port in self.neighbors.keys():
            for dst in self.dv.keys():
                if self.paths.has_key(dst):
                    if self.paths[dst][0] == port:
                        continue
                self.send(basics.RoutePacket(dst, self.dv[dst]), port)
