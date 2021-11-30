import sys
import time
import os
import threading

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
        self.send_msgs_thread = threading.Thread(target=self._distribute_msgs, daemon=True, name='distribute_msgs_thread')
    

    def start_distribute(self):
        self.send_msgs_thread.start()

    def _send_msg(self, msg, msg_size):
        buf = bytearray(msg_size)
        super().send(msg, buf)
    
    def _generate_msg(self, seq_number):
        pass

    def _distribute_msgs(self):
        msg_num = 1
        while True:
            msg = self._generate_msg(msg_num)
            self._send_msg(msg, self.msg_size)
            print(f"send {self.__str__()} msg num:{msg.header.message_seq_number}")
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

    def __str__(self):
        return "Eas msg"

class OpticMsgsDistributer(MsgsDistributer):
    def __init__(self, name, ip, port, msg_size):
        super().__init__(name, ip, port, msg_size)

    def _generate_msg(self, seq_number):
        curr_time = int(time.time() * 1000)
        header = MsgHeader(Opcode.OPTICAL_MSG, message_seq_number=seq_number)
        fire_event = FireEvent(curr_time, 1, EventType.MuzzleFlash, WeaponType.Rifle, 20, 10, 90)
        fire_events_msg = FireEventsMsg(header, curr_time, [fire_event])
        
        return fire_events_msg

    def __str__(self):
        return "Optic msg"

if __name__ == "__main__":

    eas_msgs_distributer = EASMsgsDistributer(
        "eas_msgs_distributer", "172.28.20.52", 65432, FireEventsMsg.my_size())
    optic_msgs_distributer = OpticMsgsDistributer(
        "optic_msgs_distributer", "172.28.20.52", 65433, FireEventsMsg.my_size())

    eas_msgs_distributer.start_distribute()
    optic_msgs_distributer.start_distribute()

    time.sleep(1000)