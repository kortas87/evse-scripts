#!/usr/bin/python3
import sys
import serial
import time
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException

if (len(sys.argv) < 2):
    print("please use /dev/ttyUSBx as argument")
    quit()

print("opening {} hit CTRL+C to exit".format(sys.argv[1]))
serialClient = ModbusSerialClient(method = "rtu", port=sys.argv[1], baudrate=9600, stopbits=1, bytesize=8, timeout=0.2)
serialClient.connect()

print("Trying to read register 1000 and search for EVSE on bus.")
noResponse=0
found=0
try:
    for cycle in range(1,255):
        try:
            if not serialClient.is_socket_open():
                #print("...reconnecting...")
                serialClient.connect() 
            
            rq = serialClient.read_holding_registers(1000,1,unit=cycle)
            if hasattr(rq, 'registers'):
                print("Found address {} register 1000={}".format(cycle,rq.registers[0]))
                found += 1
            else:
                print("{} no answer".format(cycle))
                noResponse += 1
                                 
        except ModbusIOException as e:
            print("{} no answer (IO exception)".format(cycle))
            noResponse += 1
            continue
        except Exception as e:
            print("error when sending or receiving bytes: {}\n{}".format(rq,str(e)))
            serialClient.close()
            time.sleep(1)
            continue
except KeyboardInterrupt:
    print('interrupted!')


if serialClient.is_socket_open():
    serialClient.close()

print("\nSCRIPT FINISHED: slaves checked: {} FOUND: {}".format(noResponse+found, found))
