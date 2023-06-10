from network import UdpNetwork
from serialization import test_functions
import json
import os
import logging as log

log.basicConfig(level=log.INFO)


HOST = '0.0.0.0'
DEFAULT_PORT = 2000

def handle_request(sock, message, address):
    try:
        request = json.loads(message)
        request_type = request.get("type", "")
        if request_type == "result":
            log.info(f"Sending {request['result']} to {request['client']}")
            sock.sendto(request["result"].encode(), tuple(request["client"]))
            return
    except:
        return

    request = {"client": address}
    if request_type not in benchmark_addresses:
        return

    benchmarker = benchmark_addresses[request_type]

    log.info(f"Sending {request} to {benchmarker}")
    sock.sendto(json.dumps(request).encode(), benchmarker)


PORT = int(os.getenv("PORT", DEFAULT_PORT))

benchmark_addresses = dict()
for format in test_functions:
    port = os.getenv(f"{format}_PORT")
    if port is not None:
        benchmark_addresses[format] = (format.lower(), int(port))

multicast_host = os.getenv("MULTICAST_HOST")
multicast_port = os.getenv("MULTICAST_PORT")
if multicast_host is not None and multicast_port is not None:
    benchmark_addresses["ALL"] = (multicast_host, int(multicast_port))

net = UdpNetwork()
net.add_socket(HOST, PORT)
log.info(f"Proxy listening to {HOST}:{PORT}")
net.run(handle_request)