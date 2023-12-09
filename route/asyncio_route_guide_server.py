import asyncio
import logging
import sys
from typing import AsyncIterable, Iterable

import grpc

import route_guide_pb2_grpc, route_guide_resources, route_guide_pb2

def get_feature(
        feature_db: Iterable[route_guide_pb2.Feature], point: route_guide_pb2.Point
) -> route_guide_pb2.Feature | None:
    """Returns Feature at given location or None."""
    for feature in feature_db:
        if feature.location == point:
            return feature
    return None


class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
    def __init__(self) -> None:
        self.db = route_guide_resources.read_route_guide_database()

    def GetFeature(
            self, request, context
    ) -> route_guide_pb2.Feature:
        feature = get_feature(self.db, request)
        if feature is None:
            return route_guide_pb2.Feature(name="", location=request)
        else:
            return feature


async def serve() -> None:
    server = grpc.aio.server()
    route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), server
    )
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    await server.start()
    print(f"listen on port: {port}")
    await server.wait_for_termination()

async def my_coroutine():
    print("Start")
    await asyncio.sleep(1)
    print("End")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    #https://bobbyhadz.com/blog/deprecationwarning-there-is-no-current-event-loop
    # if sys.version_info < (3, 10):
    #     loop = asyncio.get_event_loop()
    # else:
    #     try:
    #         loop = asyncio.get_running_loop()
    #     except RuntimeError:
    #         loop = asyncio.new_event_loop()
    #
    #     asyncio.set_event_loop(loop)

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(serve())

    asyncio.run(serve())
