from naming import get_rollercoaster_names
from park_fixtures import Attraction


def get_attractions_1():
    names = get_rollercoaster_names(3)
    attractions = [
        Attraction(names[0], duration_ticks=2, capacity=20),
        Attraction(names[1], duration_ticks=1, capacity=15),
        Attraction("It's too small a world", duration_ticks=6, capacity=30),
        Attraction(names[2], duration_ticks=1, capacity=30),
    ]
    return attractions
