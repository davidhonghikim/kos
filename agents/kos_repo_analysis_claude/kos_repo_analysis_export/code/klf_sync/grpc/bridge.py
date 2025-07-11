import grpc
from concurrent import futures
from klf.logger import log

class GRPCServer:
    def __init__(self, port=50051):
        self.port = port
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    def start(self):
        log("info", f"Starting gRPC server on port {self.port}")
        self.server.add_insecure_port(f"[::]:{self.port}")
        self.server.start()
        self.server.wait_for_termination() 