import sys
import os
import time
import threading
from tcp_comm import TcpServer
from sensors_icd import *

testdir = os.path.dirname(__file__)
srcdir = '..'
path = os.path.abspath(os.path.join(testdir, srcdir))
sys.path.insert(0, path)

from events_queue_manager import EventsManager

class SensorComm():
    def __init__(self, name, ip, port, msg_buffer_size, events_manager:EventsManager):
        self.tcp_server = TcpServer(name, ip, port)
        self.msg_buffer_size = msg_buffer_size
        self.events_manager = events_manager
        self.comm_thread = threading.Thread(target=self._start_recieving, daemon=True, name='recieving_thread')

    def start(self):
        self.comm_thread.start()

    def _start_recieving(self):
        connection, addr = self.tcp_server.connect()
        while True:
            msg_recieved = connection.recvfrom(self.msg_buffer_size)[0]
            msg = FireEventsMsg.from_bytes_array(msg_recieved, 0)
            print(f"recieved msg {Opcode(msg.header.opcode)} {msg.header.message_seq_number} {msg.events_time_ms}")
            self.events_manager.add_fire_msg(msg)

       
if __name__ == "__main__":

    events_manager = EventsManager(2000)
    eas_server = SensorComm("server", '172.28.20.52', 65432, FireEventsMsg.my_size(), events_manager)
    optic_server = SensorComm("server", '172.28.20.52', 65433, FireEventsMsg.my_size(), events_manager)

    eas_server.start()
    optic_server.start()
    time.sleep(1000)
    