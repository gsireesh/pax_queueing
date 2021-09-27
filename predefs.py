import random

from agents import FixedItineraryGuest
from naming import get_person_name, get_rollercoaster_names
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


def get_itinerary_guests(n_guests, attractions, attraction_weights=None):
    return [
        FixedItineraryGuest(
            get_person_name(),
            itinerary=random.choices(
                attractions, k=random.randint(1, len(attractions)), weights=attraction_weights
            ),
        )
        for i in range(n_guests)
    ]
