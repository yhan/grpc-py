import route_guide_resources
from route import route_guide_pb2


class ReadResources:
    def __init__(self):
        self.db = route_guide_resources.read_route_guide_database()

    def GetFeature(self):
        return self.db

def run():
    reader = ReadResources()
    features = reader.GetFeature()
    for f in features:
        print(f)

def unit():
    point = route_guide_pb2.Point(latitude=0, longitude=-0)
    print(f"{point.latitude} / {point.longitude}")

if __name__ == "__main__":
    unit()