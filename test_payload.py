#!/usr/bin/python3
import sys
import serial
import time

if (len(sys.argv) < 4):
    print("please use /dev/ttyUSBx and payload.txt and number of cycles as argument")
    quit()

def connect():
    try:
        serialPort.open()
    except Exception as e:
        print("Could not connect: {}".format(str(e)))
        return False
        
    print("Connected")
    return True

class Test:
    send = bytes()
    receive = bytes()
    text = ""
    def __init__(self, linegroup, linenumber):
        #print(linegroup[1].replace(" ", ""))
        #print(linegroup[2].replace(" ", ""))
        try:
            self.send    = bytes.fromhex(linegroup[1].replace(" ", "").strip())
            if linegroup[2].replace(" ", "").strip() == "?":
                self.receive = "?"
            else:
                self.receive = bytes.fromhex(linegroup[2].replace(" ", "").strip())
        except ValueError as e:
            print("Error parsing at line number: {}, details: {}".format(linenumber, str(e)))
        
        self.text = linegroup[0][1:].strip()
        #print("({}) in: {}, out: {}".format(self.text, self.send.hex(), self.receive.hex()))

print("opening {}, {}".format(sys.argv[1], sys.argv[2]))
serialPort = serial.Serial(port=sys.argv[1],baudrate=9600,stopbits=1, bytesize=8, timeout = 0.15)

tests = []

linegroup = [0]*3
counter = 0
linecounter = 0
with open(sys.argv[2]) as inputfile:
    for line in inputfile:
        linecounter += 1
        if ("#" == line[1:2]):
            linegroup[counter] = line
            counter += 1
        else:
            linegroup[counter] = line
            counter += 1
            if(counter>2):
                tests.append(Test(linegroup,linecounter))
                counter = 0
                
print("Payload file loaded, total {} lines, {} tests. Now TESTING:\n".format(linecounter, len(tests)))

okCount = 0
failCount = 0
for i in range(0,int(sys.argv[3])):
    print("CYCLE {}".format(i+1))
    for test in tests:
        try:
            if serialPort.isOpen():
                #perform test
                #mdbclass.calcString(.....)
                num = serialPort.write(test.send)
                #print("number of bytes written: {}".format(num))
                rxBytes = serialPort.read(20)

                #compare for ?
                if ("?" == test.receive):
                    val = 0
                    if (len(rxBytes) > 0):
                        result = "OK"
                        okCount += 1
                        val = int.from_bytes(rxBytes[3:7], 'big')/10
                    else:
                        result = "FAIL"
                        failCount += 1
                    print("{} ({}) tx: {} rx: {} expected: {}, value: {}".format(result, test.text,test.send.hex(), rxBytes.hex(), "any", val))
                #compare bytes
                else:                    
                    if(rxBytes == test.receive):
                        result = "OK"
                        okCount += 1
                    else:    
                        result = "FAIL"
                        failCount += 1
                    print("{} ({}) tx: {} rx: {} expected: {}".format(result, test.text,test.send.hex(), rxBytes.hex(), test.receive.hex()))
            else:
                print("CONNECTING, test was skipped! ({})".format(test.text))
                failCount += 1
                connect()
            

        except Exception as e:
            print("error when sending or receiving bytes, SKIPPING THIS TEST: {}, detail: {}".format(test.text, str(e)))
            serialPort.close()
            time.sleep(1)
            continue

if serialPort.isOpen():
    serialPort.close()

print("\nTEST FINISHED: OK: {} FAIL: {}".format(okCount, failCount))
