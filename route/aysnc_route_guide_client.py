import asyncio
import logging
import sys
import threading

import grpc
import route_guide_pb2
import route_guide_pb2_grpc
import route_guide_resources
from route.ThreadDiag import *
from route.route_guide_pb2_grpc import RouteGuideStub


async def guide_get_one_feature(
        stub: route_guide_pb2_grpc.RouteGuideStub, point: route_guide_pb2.Point
) -> None:
    print(thread_info() + " <- " + "guide_get_one_feature")
    feature = await stub.GetFeature(point)
    if not feature.location:
        print("Server returned incomplete feature")
        return

    if feature.name:
        print(f"Feature called {feature.name} at {feature.location}")
    else:
        print(f"Found no feature at {feature.location}")


async def guide_get_feature(stub: route_guide_pb2_grpc.RouteGuideStub) -> None:
    # The following two coroutines will be wrapped in a Future object
    # and scheduled in the event loop so that they can run concurrently
    print(thread_info() + " <- " + "guide_get_feature")
    task_group = asyncio.gather(
        guide_get_one_feature(
            stub,
            route_guide_pb2.Point(latitude=409146138, longitude=-746188906),
        ),
        guide_get_one_feature(
            stub, route_guide_pb2.Point(latitude=0, longitude=0)
        ),
    )
    # Wait until the Future is resolved
    await task_group


async def main() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub: RouteGuideStub = route_guide_pb2_grpc.RouteGuideStub(channel)

        print("-------------- GetFeature --------------")
        await guide_get_feature(stub)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
