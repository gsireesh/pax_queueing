from collections import defaultdict
from typing import Dict, List


class Attraction:
    def __init__(self, name: str, duration_ticks: int, capacity: int, park=None):
        self.name = name
        self.duration_ticks = duration_ticks
        self.capacity = capacity
        self.park = park

        self.queue = []
        self.riders = []
        self.ticks_left_until_turnover = 0

    def accept_guest(self, guest):
        self.queue.append(guest)

    def tick(self):
        if self.ticks_left_until_turnover == 0:
            # get people off of the ride
            for rider in self.riders:
                rider.last_ride = self
                self.park.liminal_space.accept_guest(rider)

            # get new people on the ride
            self.riders = []
            for i in range(self.capacity):
                if len(self.queue) != 0:
                    self.riders.append(self.queue.pop())
            self.ticks_left_until_turnover = self.duration_ticks

        for rider in self.queue:
            rider.log_tick(self.name)

        self.ticks_left_until_turnover -= 1

    def to_string(self, detailed=False):
        return f"""
{self.name}
{'-' * len(self.name)}
People in line: {', '.join([rider.name for rider in self.queue])}
People on the ride: {', '.join([rider.name for rider in self.riders])}
Time until turnover: {self.ticks_left_until_turnover}
"""


class LiminalSpace():
    def __init__(self, park):
        self.guest_to_time_left: Dict["Guest", int] = {}
        self.description = "In between rides"
        self.park = park

    def accept_guest(self, guest: "Guest"):
        next_ride = guest.plan(self.park)
        distance_to_next_ride = self.park.get_distance(guest.last_ride, next_ride)
        self.guest_to_time_left[guest] = distance_to_next_ride

    def tick(self):
        # first, decide on a next destination for each guest
        # they can:
        # - pick a new destination, at which point we start counting them down until we put them in that space
        # - put off picking a new destination, in which case we just skip them

        new_guest_to_time_map = {}
        for guest, time_left in self.guest_to_time_left.items():
            guest.log_tick(self.description)
            if time_left == 0 and guest.next_ride == self:
                next_ride = guest.plan(self.park)
                if next_ride == self:
                    continue
                distance_to_next_ride = self.park.get_distance(guest.last_ride, next_ride)
                new_guest_to_time_map[guest] = distance_to_next_ride
            elif time_left == 0:
                ride = guest.next_ride
                ride.accept_guest(guest)
            else:
                new_guest_to_time_map[guest] = time_left - 1

        self.guest_to_time_left = new_guest_to_time_map

    def to_string(self, detailed=False):
        destination_map = defaultdict(lambda: [])
        for guest, time in self.guest_to_time_left.items():
            destination_map[guest.next_ride].append((guest, time))
        return "\n".join(
            f"Heading to {next_ride.name if next_ride else 'nowhere'}: {', '.join([str(guest) for guest in guests])}"
            for next_ride, guests in destination_map.items())


class Park():
    def __init__(self, attractions: List[Attraction]):
        self.attractions = attractions
        for attraction in self.attractions:
            attraction.park = self
        self.liminal_space = LiminalSpace(self)
        self.guests = []

    def accept_guest(self, guest):
        self.guests.append(guest)
        self.liminal_space.accept_guest(guest)

    def tick(self):
        self.liminal_space.tick()
        for attraction in self.attractions:
            attraction.tick()

    def get_distance(self, thing1, thing2):
        if thing1 == thing2:
            return 0
        elif thing1 == self.liminal_space or thing2 == self.liminal_space:
            return 1
        elif thing1 is None or thing2 is None:
            return 1
        else:
            return 2

    def to_string(self, detailed=False):
        attractions_string = '\n'.join([attraction.to_string(detailed=detailed) for attraction in self.attractions])
        whole_string = f"""
LIMINAL SPACE
-------------
{self.liminal_space.to_string()}

ATTRACTIONS
-----------
{attractions_string}
"""
        return whole_string
