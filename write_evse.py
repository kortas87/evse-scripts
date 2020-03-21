#!/usr/bin/python3
import sys
import serial
import time
from pymodbus.client.sync import ModbusSerialClient

if (len(sys.argv) < 5):
    print("please use /dev/ttyUSBx, slave address (1-255), register address, value as argument")
    quit()


#, sys.argv[2], sys.argv[3]), sys.argv[4]
print("opening {} slave: {} register: {} = {}".format(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]))
serialClient = ModbusSerialClient(method = "rtu", port=sys.argv[1], baudrate=9600, stopbits=1, bytesize=8, timeout=0.3)


try:
    serialClient.connect()
    rq = serialClient.write_registers(int(sys.argv[3]), int(sys.argv[4]),unit=int(sys.argv[2]))
    print(rq)
    
except Exception as e:
    print("error when sending or receiving bytes: {}".format(str(e)))
        
        
if serialClient.is_socket_open():
    serialClient.close()

print("\nSCRIPT FINISHED")
