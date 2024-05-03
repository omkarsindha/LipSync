import phabrixlib
import ahttp
import socket
import time


def set_device_setting(http, param):
    op = http.set_cfgjson("172.17.223.170", param, path='/cgi-bin/cfgjsonrpc', version='2.0', jsonId=None,
                          https=False, queue=None, callback=None, timeout=4.0, block=True)


def get_device_setting(http, param):
    op = http.get_cfgjson("172.17.223.170", param, path='/cgi-bin/cfgjsonrpc', version='2.0', jsonId=None,
                          https=False, queue=None, callback=None, timeout=4.0, block=True)
    return op.result


class Test:
    http = ahttp.start()  # Starting http to connect to the webpage
    phabrix = phabrixlib.Phabrix(IP='172.17.223.162', port=2100, timeout=2.0,
                                 encoding='utf8')  # Connecting to the phabrix

    port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port.connect(('172.17.223.175', 4012))  # Connecting to magnum interface for routing
    port.settimeout(3)
    print('CONNECTED TO MAGNUM INTERFACE')

    # Setting the phabrix out to AV delay
    phabrix.SetValue(ID="COM_GEN1_PATTERN_SEL", value=3)

    # Setting the standard on phabrix
    for x in range(3):
        if x == 0:
            phabrix.SetValue(ID="COM_GEN1_LINK_TYPE", value=1)  # HD 720p59.94
            time.sleep(0.5)
            phabrix.SetValue(ID="COM_GEN1_LINES", value=2)  # 720p
            time.sleep(0.5)
            phabrix.SetValue(ID="COM_GEN1_RATE", value=6)  # 59.94
            cmd = '.SVABCDEFGHIJKLMNOPQRS%03d,%03d\r' % (1, 3)
            port.send(cmd.encode())
        elif x == 1:
            phabrix.SetValue(ID="COM_GEN1_LINK_TYPE", value=1)  # HD 1080i59.94
            time.sleep(0.5)
            phabrix.SetValue(ID="COM_GEN1_LINES", value=4)  # 1080i
            time.sleep(0.5)
            phabrix.SetValue(ID="COM_GEN1_RATE", value=6)  # 59.94
            cmd = '.SVABCDEFGHIJKLMNOPQRS%03d,%03d\r' % (1, 7)
            port.send(cmd.encode())
        elif x == 2:
            phabrix.SetValue(ID="COM_GEN1_LINK_TYPE", value=3)  # 3G 1080p59.94
            time.sleep(0.5)
            phabrix.SetValue(ID="COM_GEN1_LINES", value=6)
            time.sleep(0.5)
            phabrix.SetValue(ID="COM_GEN1_RATE", value=6)
            cmd = '.SVABCDEFGHIJKLMNOPQRS%03d,%03d\r' % (1, 13)
            port.send(cmd.encode())
        # Looping the value between 0 and 1 (Bypass and timestamp)
        for m in range(2):
            set_device_setting(http, {'816.0@i': m})
            # Setting vertical offset
            for n in range(2):
                if n == 0:
                    set_device_setting(http, {'159.0@i': 0})
                if n == 1:
                    set_device_setting(http, {'159.0@i': 4})
                # Setting the AES67IP
                for o in range(2):
                    set_device_setting(http, {'638@i': o})
                    # Checking if all the values are set
                    outputAV = get_device_setting(http, ['816.0@i'])['816.0@i']
                    voffset = get_device_setting(http, ['159.0@i'])['159.0@i']
                    aes = get_device_setting(http, ['638@i'])['638@i']
                    format = f"{phabrix.get_text(560)} "
                    # Setting complete now reading the left and right value
                    time.sleep(3)
                    left_measurement = phabrix.GetText(2402)
                    right_measurement = phabrix.GetText(2403)

                    print(f"Values are OutputAV: {outputAV} Vertical Offset: {voffset} AES: {aes}")
                    print(f"Format on phabrix: {format}")
                    print(f"Phabrix Delay Right {right_measurement} Left {left_measurement}\n\n")

    phabrix.close()
