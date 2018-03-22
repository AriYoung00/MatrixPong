from threading import Thread

import bluetooth
import time


server = None
has_init = False


def init_server():
    global has_init
    global server

    if has_init:
        print("Only call init_server once")
        return

    server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    server.bind(("", bluetooth.PORT_ANY))
    server.listen(2)
    print("Listening for bluetooth connections on port %d" % server.port)

    bluetooth.advertise_service(server, "MatrixPong")
    has_init = True


def scan_bluetooth_devices(timeout=10):
    return bluetooth.discover_devices(duration=timeout, flush_cache=True, lookup_names=True)
 


class PongPlayerThread(Thread):
    paddle = None

    client_sock = bluetooth.BluetoothSocket()
    client_addr = None

    client_max_y = None


    def __init__(self, paddle):
        self.paddle = paddle


    def pair_with_phone(self):
        global server

        raw = server.accept()
        self.client_sock = bluetooth.BluetoothSocket() # TODO: switch this and initial assignment back to proper values
        self.client_addr = raw[1]

        print("Accepted connection from address %s" % self.client_addr)


    def run(self):
        self.client_max_y = self._parse_data(self.client_sock.recv(2))

        if self.client_max_y == None:
            print("Received invalid max y value, exiting")
            raise(ValueError("Corrupt max value from client"))


        while True:
            current_value = self._parse_data(self.client_sock.recv(2))
            if current_value == None:
                return

            move_pos = (current_value / self.client_max_y) * 32
            self.paddle.set_pos((move_pos, self.paddle.pos[1]))

            time.sleep(0.01)


    def _parse_data(data):
        if type(data) == int:
            return data
        else:
            try:
                return int(data)
            except ValueError:
                print("Received corrupt communication from client, ignoring")
                return None


    def __str__(self):
        return "PongPlayerThread, with bluetooth connection to %s, and paddle at %s" % (self.client_addr, self.paddle.pos)


    def __repr__(self):
        return self.__str__()