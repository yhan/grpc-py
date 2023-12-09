import logging
from concurrent import futures

import grpc

import route_guide_pb2_grpc
import route_guide_resources
import route_guide_pb2
from route_guide_pb2 import *


def get_feature(feature_db: list[Feature], point: Point):
    for f in feature_db:
        if f.location == point:
            return f
    return None


class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        self.db = route_guide_resources.read_route_guide_database()

    def GetFeature(self, point, context):
        feature = get_feature(self.db, point)
        if feature is None:
            return Feature(name="", location=point)
        else:
            return feature


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), server
    )
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()