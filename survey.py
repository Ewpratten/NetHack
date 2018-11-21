"""Outputs the ordered list of the most powerful WiFi devices based on signal."""
import time
import heapq
import curses
import os
import math

__author__ = 'Caleb Madrigal'
__email__ = 'caleb.madrigal@gmail.com'
__version__ = '0.0.6'
__apiversion__ = 1
__config__ = {'power': -100, 'log_level': 'ERROR', 'trigger_cooldown': 1}

DEVS_TO_IGNORE = {'ff:ff:ff:ff:ff:ff', '00:00:00:00:00:00'}

def calculateDistance(signalLevelInDb, freqInMHz):
    exp = (27.55 - (20 * Math.log10(freqInMHz)) + Math.abs(signalLevelInDb)) / 20.0
    return Math.pow(10.0, exp)

class Trigger:
    def __init__(self):
        self.dev_to_power = {}
        self.dev_to_vendor = {}
        self.dev_to_last_seen = {}
        self.frame_count = 0
        self.devices = {"data":[]}


    def __call__(self, dev_id=None, dev_type=None, power=None, vendor=None, **kwargs):
        # Only look at individual devices (device and bssids), and only look when power is present
        if (not power) or (not dev_id) or (dev_type == 'ssid') or (dev_id in DEVS_TO_IGNORE):
            return
        
        first = ""
        add = True
        for dev in self.devices["data"]:
            if dev["mac"] == dev_id:
                add = False
        
        if add:
            self.devices["data"].append({"mac":dev_id,"vendor": vendor, "readings":[]})
            first = " @"
        
        i = 0
        for dev in self.devices["data"]:
        	if dev["mac"] == dev_id:
        		self.devices["data"][i]["readings"].append([power, time.time()])
        	i += 1
        
        print(f"Device: {dev_id} "+ str(power) + first)


    def __del__(self):
        with open("./survout-"+str(time.time())+".json", "a+") as f:
        	f.writelines(str(self.devices))
        	f.close()

if __name__ == '__main__':
    # Smoke test
    t = Trigger()
    for i in range(100):
        t(dev_id=i, power=i)
        time.sleep(.1)
