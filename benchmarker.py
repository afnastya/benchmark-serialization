from network import UdpNetwork
from serialization import *
import timeit
import os
import logging as log

log.basicConfig(level=log.INFO)

DEFAULT_FORMAT = "JSON"
HOST = '127.0.0.1'
DEFAULT_PORT = 2001
TEST_NUMBER = 10000

def handle_request(sock, message, address):
    request = from_json(message)
    print(type(request))

    from_format, to_format = test_functions[FORMAT]
    format_data = to_format(test_data)

    timer = timeit.Timer(lambda: from_format(format_data))
    serialization_time = timer.timeit(TEST_NUMBER)
    serialization_time = round(serialization_time, 2)

    timer = timeit.Timer(lambda: to_format(test_data))
    deserialization_time = timer.timeit(TEST_NUMBER)
    deserialization_time = round(deserialization_time, 2)

    result = f"{FORMAT}-{serialization_time}ms-{deserialization_time}ms\n"

    responce = request
    responce["type"] = "result"
    responce["result"] = result

    log.info(f"Sending {responce} to {address}")
    sock.sendto(json.dumps(responce).encode(), address)


FORMAT = os.getenv("FORMAT", DEFAULT_FORMAT)
if FORMAT not in test_functions:
    os.exit(1)
PORT = int(os.getenv("PORT", DEFAULT_PORT))
HOST = FORMAT.lower()

multicast_host = os.getenv("MULTICAST_HOST")
multicast_port = os.getenv("MULTICAST_PORT")

net = UdpNetwork()
net.add_socket(HOST, PORT)
log.info(f"Benchmarker {FORMAT}. Listening to {HOST}:{PORT}")

if multicast_host is not None and multicast_port is not None:
    net.add_socket(multicast_host, int(multicast_port), 'multicast')
    log.info(f"Benchmarker {FORMAT}. Listening to {multicast_host}:{multicast_port}")

net.run(handle_request)
