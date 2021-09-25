from agents import Guest
from park_fixtures import Attraction, Park


def main():
    attractions = [Attraction("Lightning Inferno", 3, 20, None)]
    park = Park(attractions)

    guests = [Guest("Frank")]
    park.accept_guest(guests[0])

    for i in range(25):
        print(park.to_string())
        print("============================================")
        park.tick()


if __name__ == '__main__':
    main()
