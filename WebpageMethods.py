def set_device_setting(http, ip, param):
    op = http.set_cfgjson(ip, param, path='/cgi-bin/cfgjsonrpc', version='2.0', jsonId=None,
                          https=False, queue=None, callback=None, timeout=4.0, block=True)

def get_device_setting(http,ip, param):
    op = http.get_cfgjson(ip, param, path='/cgi-bin/cfgjsonrpc', version='2.0', jsonId=None,
                          https=False, queue=None, callback=None, timeout=4.0, block=True)
    return op.result
