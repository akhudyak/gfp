import enum
import time
from struct import *

class EventType(int, enum.Enum):
    MuzzleFlash = 0
    ShockWave = 1
    MuzzleBlast = 2


class WeaponType(int, enum.Enum):
    Unknown = 0
    Handgun = 1
    Rifle = 2
    Sniper = 3

class Opcode(int, enum.Enum):
    KEEP_ALIVE = 0
    ACOUSTIC_MSG = 1
    OPTICAL_MSG = 2

class MsgHeader:
    def __init__(self, opcode, source_id=1, message_body_length=1, message_seq_number=1):
        self.opcode = opcode
        self.source_id = source_id
        self.message_body_length = message_body_length
        self.message_seq_number = message_seq_number

    @staticmethod
    def my_size():
        return calcsize("=HHIH")

    def to_bytes_array(self, buf, offset):
        cur_offset = offset
        pack_into("<HHIH", buf, cur_offset, self.opcode, self.source_id,
                  self.message_body_length, self.message_seq_number)

    @staticmethod
    def from_bytes_array(buf, offset):
        obj = unpack_from("<HHIH", buf, offset)
        header = MsgHeader(obj[0], obj[1], obj[2], obj[3])
        return header

class FireEvent:
    def __init__(self, time_millisec, time_in_samples, event_type, weapon_type, aoa, elevation, event_confidence):
        self.time_millisec = time_millisec  # unsigned long long
        self.time_in_samples = time_in_samples  # ushort
        self.event_type = event_type  # uchar
        self.weapon_type = weapon_type  # uchar
        self.aoa = aoa  # uint
        self.elevation = elevation  # int
        self.event_confidence = event_confidence  # uint

    @staticmethod
    def my_size():
        return calcsize("=QHBBIiI")

    def to_bytes_array(self, buf, offset):
        cur_offset = offset
        pack_into("<QHBBIiI", buf, cur_offset, self.time_millisec, self.time_in_samples, self.event_type, self.weapon_type,
                  self.aoa, self.elevation, self.event_confidence)
    
    @staticmethod
    def from_bytes_array(buf, offset):
        obj = unpack_from("<QHBBIiI", buf, offset)
        fire_event = FireEvent(obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6])
        return fire_event

class FireEventsMsg:
    def __init__(self, header, events_time_ms, events):
        self.header = header
        self.msg_size_bytes = self.my_size()  # int
        self.events_count = len(events)  # int
        self.events_time_ms = events_time_ms  # int
        self.events = events

    @staticmethod
    def my_size():
        return 822

    def to_bytes_array(self, buf, offset):
        cur_offset = offset
        self.header.to_bytes_array(buf, cur_offset)
        cur_offset += MsgHeader.my_size()
        pack_into("<iiQ", buf, cur_offset, self.msg_size_bytes, self.events_count, self.events_time_ms)
        cur_offset += calcsize("=iiQ")
        for i in range(0, self.events_count):
            self.events[i].to_bytes_array(buf, cur_offset)
            cur_offset += self.events[i].my_size()

    @staticmethod
    def from_bytes_array(buf, offset):
        header = MsgHeader.from_bytes_array(buf, offset)
        obj = unpack_from("<iiQ", buf, MsgHeader.my_size())
        msg_size_bytes = obj[0]
        events_count = obj[1]
        events_time_ms = obj[2]

        offset+=MsgHeader.my_size()
        offset+=calcsize("=iiQ")
        events = []
        for i in range (0, events_count):
            fire_event = FireEvent.from_bytes_array(buf, offset)
            events.append(fire_event)
            offset+=FireEvent.my_size()

        fire_events_msg = FireEventsMsg(header, events_time_ms, events)
        return fire_events_msg


if __name__ == "__main__":
    curr_time = int(time.time() * 1000)
    fire_event = FireEvent(curr_time, 1, EventType.MuzzleFlash, WeaponType.Rifle, 20, 10, 90)
    buf = bytearray(FireEvent.my_size())
    fire_event.to_bytes_array(buf,0)
    unpacked_event =  FireEvent.from_bytes_array(buf, 0)

    fire_events_msg = FireEventsMsg(MsgHeader(Opcode.ACOUSTIC_MSG), curr_time, [fire_event])
    buf = bytearray(FireEventsMsg.my_size())
    fire_events_msg.to_bytes_array(buf, 0)
    unpacked_msg = FireEventsMsg.from_bytes_array(buf, 0)
    print("end")