import random

from agents import Guest, QueueLengthGuest
from naming import get_person_name
from park_fixtures import Park
from predefs import get_attractions_1, get_itinerary_guests

N_GUESTS = 400
N_ATTRACTIONS = 3

random.seed(234)

attractions = get_attractions_1()
park = Park(attractions)

guests = (
    [Guest(get_person_name()) for i in range(200)]
    + [QueueLengthGuest(get_person_name()) for i in range(200)]
    + get_itinerary_guests(4, attractions)
)
for guest in guests:
    park.accept_guest(guest)

for i in range(25):
    # print(park.to_string())
    # print("============================================")
    park.tick()
    # sleep(1)
print(park.get_guest_report())
