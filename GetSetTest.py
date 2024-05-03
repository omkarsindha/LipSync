import phabrixlib

phabrix = phabrixlib.Phabrix(IP='172.17.223.162', port=2100, timeout=2.0,
                             encoding='utf8')  # Connecting to the phabrix
i = 1

value = (phabrix.get_text(560))
print(f"{i} = {value}")
    # if value == '1080i59':
    #     print(i)
    #     break
    # i += 1
# print(phabrix.set_value(ID=36, value=1))
