from agents import Guest
from naming import get_person_name
from park_fixtures import Park
from predefs import get_attractions_1

N_GUESTS = 400
N_ATTRACTIONS = 3


def main():
    attractions = get_attractions_1()
    park = Park(attractions)

    guests = [Guest(get_person_name()) for i in range(N_GUESTS)]
    for guest in guests:
        park.accept_guest(guest)

    for i in range(25):
        # print(park.to_string())
        # print("============================================")
        park.tick()
        # sleep(1)

    print(guests[0].get_day_log())
    print(guests[0].get_day_breakdown_string())

    print(park.get_guest_report())


if __name__ == "__main__":
    main()
