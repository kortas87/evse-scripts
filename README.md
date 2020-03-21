
#prerequisites:
pip3 install pymodbus

#Read all data from EVSE (UART or RS485):
python3 read_evse.py /dev/ttyUSB0 1

#Write data to EVSE (set default max current to 26A):
python3 write_evse.py /dev/ttyUSB0 1 2000 26

#Discover EVSE on bus (check 1-255 addresses)
python3 discover_evse.py

#run EVSE test 10x:
python3 test_payload.py /dev/ttyUSB0 payload_rs485_testing.txt 10
