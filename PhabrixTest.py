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


