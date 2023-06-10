from network import UdpNetwork
from serialization import test_functions
import json
import os
import logging as log

log.basicConfig(level=log.INFO)


HOST = '0.0.0.0'
DEFAULT_PORT = 2000

def handle_request(sock, message, address):
    request = json.loads(message)
    request_type = request["type"]
    if request_type == "result":
        log.info(f"Sending {request['result']} to {request['client']}")
        sock.sendto(request["result"].encode(), tuple(request["client"]))
        return

    format = request_type
    if format not in test_functions:
        return
    
    request = {"client": address}
    benchmarker = benchmark_addresses[format]

    log.info(f"Sending {request} to {benchmarker}")
    sock.sendto(json.dumps(request).encode(), benchmarker)


PORT = int(os.getenv("PORT", DEFAULT_PORT))

benchmark_addresses = dict()
for format in test_functions:
    port = os.getenv(f"{format}_PORT")
    if port is not None:
        benchmark_addresses[format] = (format.lower(), int(port))

net = UdpNetwork()
net.add_socket(HOST, PORT)
log.info(f"Proxy listening to {HOST}:{PORT}")
net.run(handle_request)