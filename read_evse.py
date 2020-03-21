#!/usr/bin/python3
import sys
import serial
import time
from pymodbus.client.sync import ModbusSerialClient

if (len(sys.argv) < 3):
    print("please use /dev/ttyUSBx and slave address (1-255) as argument")
    quit()

def connect():
    try:
        serialPort.open()
    except Exception as e:
        print("Could not connect: {}".format(str(e)))
        return False
        
    print("Connected")
    return True



print("opening {}, address: {} hit CTRL+C to exit".format(sys.argv[1], sys.argv[2]))
serialClient = ModbusSerialClient(method = "rtu", port=sys.argv[1], baudrate=9600, stopbits=1, bytesize=8, timeout=0.3)
serialClient.connect()

cycle=0
failCount=0
try:
    while True:
        cycle += 1
        #print("cycle: {} fails: {}".format(cycle,failCount))
        try:
            if serialClient.is_socket_open():
                if 1==cycle:
                    rq = serialClient.read_holding_registers(2000,18,unit=int(sys.argv[2]))
                    if 18 == len(rq.registers):
                        print("    EVSE config:")
                        print("2000 | default amps [A]                                  : {}".format(rq.registers[0]))
                        print("2001 | modbus address                                    : {}".format(rq.registers[1]))
                        print("2002 | minimum amps [A]                                  : {}".format(rq.registers[2]))
                        print("2003 | analog input config (0=0-5V input, 1,2,...=button): {}".format(rq.registers[3]))
                        print("2004 | save / not save amps by button                    : {}".format(rq.registers[4]))
                        print("2005 | config bits                                       : {}".format(rq.registers[5]))
                        print("  b0 | enable button (on AN input) for current change    : {}".format(rq.registers[5]&1>0))
                        print("  b1 | stop charging when button pressed                 : {}".format(rq.registers[5]&2>0))
                        print("  b2 | pilot ready state LED is not blinking             : {}".format(rq.registers[5]&4>0))
                        print("  b3 | enable charging on STATUS D                       : {}".format(rq.registers[5]&8>0))
                        print("  b4 | enable RCD feedback (MCLR pin)                    : {}".format(rq.registers[5]&16>0))
                        print("  b5 | autoclear RCD error (30s timeout)                 : {}".format(rq.registers[5]&32>0))
                        print("  .. | reserved")
                        print(" b13 | disable EVSE after charge                         : {}".format(rq.registers[5]&8192>0))
                        print(" b14 | EVSE is disabled (no charge)                      : {}".format(rq.registers[5]&16384>0))
                        print(" b15 | enable bootloader mode                            : {}".format(rq.registers[5]&32768>0))
                        print("2006 | reserved                                          : {}".format(rq.registers[6]))
                        print("2007 | PP detection limit [A]                            : {}".format(rq.registers[7]))
                        print("2008 | reserved                                          : {}".format(rq.registers[8]))
                        print("2009 | bootloader FW revision                            : {}".format(rq.registers[9]))
                        print("2010 | amps value  6A [A]                                : {}".format(rq.registers[10]))
                        print("2011 | amps value 10A [A]                                : {}".format(rq.registers[11]))
                        print("2012 | amps value 16A [A]                                : {}".format(rq.registers[12]))
                        print("2013 | amps value 25A [A]                                : {}".format(rq.registers[13]))
                        print("2014 | amps value 32A [A]                                : {}".format(rq.registers[14]))
                        print("2015 | amps value 48A [A]                                : {}".format(rq.registers[15]))
                        print("2016 | amps value 63A [A]                                : {}".format(rq.registers[16]))
                        print("2017 | amps value 80A [A]                                : {}".format(rq.registers[17]))
                        time.sleep(1)
                    else:
                        print("Could not read config (18 registers)")
                rq = serialClient.read_holding_registers(1000,8,unit=int(sys.argv[2]))
                
                if 8 == len(rq.registers):
                    print("\n   EVSE runtime variables:")
                    print("1000 | actual amps [A]                                    : {}".format(rq.registers[0]))
                    print("1001 | amps on PWM driver output [A]                      : {}".format(rq.registers[1]))
                    print("1002 | vehicle state 1=ready,2=present,3=chg,4=vent,5=err : {}".format(rq.registers[2]))
                    print("1003 | cable limit detected [A]                           : {}".format(rq.registers[3]))
                    print("1004 | commands                                           : {}".format(rq.registers[4]))
                    print("  b0 | turn off charging now                              : {}".format(rq.registers[4]&1>0))
                    print("  b1 | run RCD test procedure                             : {}".format(rq.registers[4]&2>0))
                    print("  b2 | clear RCD error                                    : {}".format(rq.registers[4]&4>0))
                    print("  .. | reserved")
                    print("1005 | firmware revision                                  : {}".format(rq.registers[5]))
                    print("1006 | EVSE state 1=12V,2=pwm,3=off                       : {}".format(rq.registers[6]))
                    print("1007 | status and fails                                   : {}".format(rq.registers[7]))
                    print("  b0 | relay on/off                                       : {}".format(rq.registers[7]&1>0))
                    print("  b1 | diode check fail                                   : {}".format(rq.registers[7]&2>0))
                    print("  b2 | vent required fail                                 : {}".format(rq.registers[7]&4>0))
                    print("  b3 | waiting for pilot release (err recovery delay)     : {}".format(rq.registers[7]&8>0))
                    print("  b4 | RCD test in progress                               : {}".format(rq.registers[7]&16>0))
                    print("  b5 | RCD check error                                    : {}".format(rq.registers[7]&32>0))
                    print("  .. | reserved")
                else:
                    print("Could not read runtime values (8 registers)")
            else:
                print("...RECONNECTING...")
                serialClient.connect()   
        except Exception as e:
            print("error when sending or receiving bytes: {}\n{}".format(rq,str(e)))
            failCount += 1
            serialClient.close()
            time.sleep(1)
            continue
        time.sleep(1)
except KeyboardInterrupt:
    print('interrupted!')


if serialClient.is_socket_open():
    serialClient.close()

print("\nSCRIPT FINISHED: CYCLES: {} FAIL: {}".format(cycle, failCount))
