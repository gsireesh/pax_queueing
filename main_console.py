import random
from time import sleep

from agents import Guest
from naming_constants import get_person_name, get_rollercoaster_names
from park_fixtures import Attraction, Park

N_GUESTS = 40
N_ATTRACTIONS = 3


def main():
    attractions = [Attraction(name, random.randint(1, 12), random.randint(2, 10), None) for name in
                   get_rollercoaster_names(N_ATTRACTIONS)]
    park = Park(attractions)

    guests = [Guest(get_person_name()) for i in range(N_GUESTS)]
    for guest in guests:
        park.accept_guest(guest)

    for i in range(25):
        print(park.to_string())
        print("============================================")
        park.tick()
        sleep(1)


if __name__ == '__main__':
    main()
