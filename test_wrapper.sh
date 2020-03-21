#!/bin/sh
cd ~GIT/evse_firmware/testing
python3 test_payload.py /dev/ttyUSB0 payload_rs485_testing.txt 10
read -p "Press any key to exit " -n1 junk
echo
