import sys
import time
import os

testdir = os.path.dirname(__file__)
srcdir = '../sensors_icd'
path = os.path.abspath(os.path.join(testdir, srcdir))
sys.path.insert(0, path)

from sensors_icd import *
from tcp_comm import TcpClient

class MsgsDistributer(TcpClient):
    def __init__(self, name, ip, port, msg_size):
        super().__init__(name, ip, port)
        self.msg_size = msg_size

    def _send_msg(self, msg, msg_size):
        buf = bytearray(msg_size)
        super().send(msg, buf)
    
    def _generate_msg(self, seq_number):
        pass

    def start_distribute_msgs(self):
        msg_num = 1
        while True:
            msg = self._generate_msg(msg_num)
            self._send_msg(msg, self.msg_size)
            print(f"send eas msg num:{msg.header.message_seq_number}")
            time.sleep(1)
            msg_num+=1

class EASMsgsDistributer(MsgsDistributer):
    def __init__(self, name, ip, port, msg_size):
        super().__init__(name, ip, port, msg_size)

    def _generate_msg(self, seq_number):
        curr_time = int(time.time() * 1000)
        header = MsgHeader(Opcode.ACOUSTIC_MSG, message_seq_number=seq_number)
        fire_event = FireEvent(curr_time, 1, EventType.ShockWave, WeaponType.Rifle, 20, 10, 90)
        fire_events_msg = FireEventsMsg(header, curr_time, [fire_event])
        
        return fire_events_msg

class OpticMsgsDistributer(MsgsDistributer):
    def __init__(self, name, ip, port, msg_size):
        super().__init__(name, ip, port, msg_size)

    def _generate_msg(self, seq_number):
        curr_time = int(time.time() * 1000)
        header = MsgHeader(Opcode.OPTICAL_MSG, message_seq_number=seq_number)
        fire_event = FireEvent(curr_time, 1, EventType.MuzzleFlash, WeaponType.Rifle, 20, 10, 90)
        fire_events_msg = FireEventsMsg(header, curr_time, [fire_event])
        
        return fire_events_msg

if __name__ == "__main__":

    msgs_distributer = EASMsgsDistributer(
        "eas_msgs_distributer", "192.168.0.79", 65432, FireEventsMsg.my_size())
    msgs_distributer.start_distribute_msgs()
