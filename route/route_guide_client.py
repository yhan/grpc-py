import logging

import grpc
import route_guide_pb2
import route_guide_pb2_grpc
import route_guide_resources
from route.route_guide_pb2_grpc import RouteGuideStub


def guide_get_feature(stub: RouteGuideStub):
    point = route_guide_pb2.Point(latitude=409146138, longitude=-746188906)
    guide_get_one_feature(stub, point) # editor does not detect signature

    point = route_guide_pb2.Point(latitude=0, longitude=-0)
    guide_get_one_feature(stub, point)  # editor does not detect signature

def guide_get_one_feature(stub, point):
    feature = stub.GetFeature(point)
    if not feature.location:
        print("Server returned incomplete feature")
        return

    if feature.name:
        print("Feature called %s at %s" % (feature.name, feature.location))
    else:
        print(f"Found no feature at featureReturned={feature.location}/ pointAsked={point}")


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub: RouteGuideStub = route_guide_pb2_grpc.RouteGuideStub(channel)

        print("-------------- GetFeature --------------")
        guide_get_feature(stub)



if __name__ == "__main__":
    logging.basicConfig()
    run()
