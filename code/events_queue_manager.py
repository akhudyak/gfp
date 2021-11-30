import threading
import time
import queue

from sensors_icd import Opcode


class TimeUnit():
    def __init__(self, start_time, end_time):
      self.start_time = start_time
      self.end_time = end_time

class MsgsContainer():
    def __init__(self, start_time):
      self.conainer_creat_time = time.time() * 1000
      self.start_time = start_time
      self.end_time = start_time
      self.eas_msgs_list = []
      self.optic_msgs_list = []

    def add_eas_msg(self, new_msg):
      self.eas_msgs_list.append(new_msg)
      if(new_msg.events_time_ms > self.end_time):
          self.end_time = new_msg.events_time_ms

    def add_optic_msg(self, new_msg):
      self.eas_msgs_list.append(new_msg)
      if(new_msg.events_time_ms > self.end_time):
            self.end_time = new_msg.events_time_ms


class EventsManager():
    def __init__(self, slot_time_ms):
      self.lock = threading.Lock()
      self.keys_list = []
      self.slot_time_ms = slot_time_ms
      self.msgs_dictionary = {}
      self.msgs_slots_list = []

    def add_fire_msg(self, new_msg):
      time = int(new_msg.events_time_ms / self.slot_time_ms)
      self.lock.acquire()
      if time not in self.msgs_dictionary.keys():
            msgs_container = MsgsContainer(new_msg.events_time_ms*1000)
            self.msgs_dictionary[time] = msgs_container
            self.msgs_slots_list.append(time)
            print(f"create MsgsContainer:{time}")

      if new_msg.header.opcode == Opcode.ACOUSTIC_MSG:
        self.msgs_dictionary[time].add_eas_msg(new_msg)
        print(f"add eas msg:{new_msg.events_time_ms}")
      else:
        if new_msg.header.opcode == Opcode.OPTICAL_MSG:
          self.msgs_dictionary[time].add_optic_msg(new_msg)
          print(f"add optical msg:{new_msg.events_time_ms}")
          
      self.lock.release()

    