import asyncio
import logging
import sys
import time
import math

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



def get_distance(
    start: route_guide_pb2.Point, end: route_guide_pb2.Point
) -> float:
    """Distance between two points."""
    coord_factor = 10000000.0
    lat_1 = start.latitude / coord_factor
    lat_2 = end.latitude / coord_factor
    lon_1 = start.longitude / coord_factor
    lon_2 = end.longitude / coord_factor
    lat_rad_1 = math.radians(lat_1)
    lat_rad_2 = math.radians(lat_2)
    delta_lat_rad = math.radians(lat_2 - lat_1)
    delta_lon_rad = math.radians(lon_2 - lon_1)

    # Formula is based on http://mathforum.org/library/drmath/view/51879.html
    a = pow(math.sin(delta_lat_rad / 2), 2) + (
        math.cos(lat_rad_1)
        * math.cos(lat_rad_2)
        * pow(math.sin(delta_lon_rad / 2), 2)
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371000
    # metres
    return R * c

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

    async def ListFeatures(
            self, request: route_guide_pb2.Rectangle, unused_context
    ) -> AsyncIterable[route_guide_pb2.Feature]:
        left = min(request.lo.longitude, request.hi.longitude)
        right = max(request.lo.longitude, request.hi.longitude)
        top = max(request.lo.latitude, request.hi.latitude)
        bottom = min(request.lo.latitude, request.hi.latitude)
        for feature in self.db:
            if (
                    feature.location.longitude >= left
                    and feature.location.longitude <= right
                    and feature.location.latitude >= bottom
                    and feature.location.latitude <= top
            ):
                yield feature

    async def RouteChat(
        self,
        request_iterator: AsyncIterable[route_guide_pb2.RouteNote],
        unused_context,
    ) -> AsyncIterable[route_guide_pb2.RouteNote]:
        prev_notes = []
        async for new_note in request_iterator:
            for prev_note in prev_notes:
                if prev_note.location == new_note.location:
                    yield prev_note
            prev_notes.append(new_note)

    async def RecordRoute(
        self,
        request_iterator: AsyncIterable[route_guide_pb2.Point],
        unused_context,
    ) -> route_guide_pb2.RouteSummary:
        point_count = 0
        feature_count = 0
        distance = 0.0
        prev_point = None

        start_time = time.time()
        async for point in request_iterator:
            point_count += 1
            if get_feature(self.db, point):
                feature_count += 1
            if prev_point:
                distance += get_distance(prev_point, point)
            prev_point = point

        elapsed_time = time.time() - start_time
        return route_guide_pb2.RouteSummary(
            point_count=point_count,
            feature_count=feature_count,
            distance=int(distance),
            elapsed_time=int(elapsed_time),
        )

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

    # https://bobbyhadz.com/blog/deprecationwarning-there-is-no-current-event-loop
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
