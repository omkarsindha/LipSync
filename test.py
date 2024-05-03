import phabrixlib
import ahttp
import socket
import time

standard = ''
outputAV = ''
voffset = ''
aes = ''
i = 1
for x in range(3):
    if x == 0:
        standard = '720P'
    elif x == 1:
        standard = '1080i'
    elif x == 2:
        standard = '1080p'

    # Looping the value between 0 and 1 (Bypass and timestamp)
    for m in range(2):
        if m == 0:
            outputAV = 'Bypass'
        elif m == 1:
            outputAV = 'Timestamp'
        # Setting vertical offset
        for n in range(2):
            if n == 0:
                voffset = '0'
            if n == 1:
                voffset = '4'
            # Setting the AES67IP
            for o in range(2):
                if n == 0:
                    aes = '125us'
                if n == 1:
                    aes = '1ms'
                time.sleep(0.5)
                print(f"{standard}\t{outputAV.ljust(9)}\t{voffset}\t{aes}")
                i += 1
