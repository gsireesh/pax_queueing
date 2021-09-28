from collections import defaultdict
from typing import Dict, List

import pandas as pd

from constants import GUEST_REP_CHAR, STATE_WAITING, STATE_RIDING


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
            rider.log_tick((self.name, STATE_WAITING))

        for rider in self.riders:
            rider.log_tick((self.name, STATE_RIDING))

        self.ticks_left_until_turnover -= 1

    def to_string(self, detailed=False):
        return f"""
{self.name}
{'-' * len(self.name)}
People in line: {', '.join([rider.name for rider in self.queue]) if detailed else GUEST_REP_CHAR * len(self.queue)}
People on the ride: {', '.join([rider.name for rider in self.riders]) if detailed else GUEST_REP_CHAR * len(self.riders)}
Time until turnover: {self.ticks_left_until_turnover}
"""


class LiminalSpace:
    def __init__(self, park):
        self.guest_to_time_left: Dict["Guest", int] = {}
        self.description = "Liminal Space"
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
            guest.log_tick((self.description, STATE_WAITING))
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

    def _stringify_guestlist(self, guestlist, detailed=False):
        return (
            ", ".join([str(guest) for guest in guestlist])
            if detailed
            else GUEST_REP_CHAR * len(guestlist)
        )

    def _get_destination_map(self):
        destination_map = defaultdict(lambda: [])
        for guest, time in self.guest_to_time_left.items():
            destination_map[guest.next_ride].append((guest, time))
        return destination_map

    def to_string(self, detailed=False):
        destination_map = self._get_destination_map()
        return "\n".join(
            f"Heading to {next_ride.name if next_ride else 'nowhere'}: {self._stringify_guestlist(guests, detailed)}"
            for next_ride, guests in destination_map.items()
        )


class Park:
    def __init__(self, attractions: List[Attraction]):
        self.attractions = attractions
        for attraction in self.attractions:
            attraction.park = self
        self.liminal_space = LiminalSpace(self)
        self.guests = []
        self.historic_state = defaultdict(lambda: [])

    def accept_guest(self, guest):
        self.guests.append(guest)
        self.liminal_space.accept_guest(guest)

    def tick(self):
        self.liminal_space.tick()
        destination_map = self.liminal_space._get_destination_map()
        # for destination, queue in destination_map.items():
        #     self.historic_state[f"liminal_space_to_{destination.name}"].append(len(queue))
        for attraction in self.attractions:
            attraction.tick()
            self.historic_state[attraction.name].append(len(attraction.queue))

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
        attractions_string = "\n".join(
            [attraction.to_string(detailed=detailed) for attraction in self.attractions]
        )
        whole_string = f"""
LIMINAL SPACE
-------------
{self.liminal_space.to_string(detailed=detailed)}

ATTRACTIONS
-----------
{attractions_string}
"""
        return whole_string

    def get_state(self):
        return self.historic_state

    def get_guest_stats_by_type(self):
        guests_by_type = defaultdict(lambda: [])
        for guest in self.guests:
            guests_by_type[type(guest)].append(guest)

        type_to_df = {}
        for guest_type, guests in guests_by_type.items():
            type_df = pd.DataFrame([guest.get_day_breakdown() for guest in guests])
            type_to_df[guest_type] = type_df
        return type_to_df

    def get_guest_report(self):
        guest_dfs = self.get_guest_stats_by_type()
        type_to_states = {}
        for guest_type, guest_df in guest_dfs.items():
            time_waiting = guest_df[STATE_WAITING].mean()
            time_riding = guest_df[STATE_RIDING].mean()
            type_to_states[guest_type] = (time_waiting, time_riding)

        return [
            f"Guests of type {str(guest_type)} spent an average of {time_waiting} ticks waiting, and {time_riding} ticks riding rides"
            for guest_type, (time_waiting, time_riding) in type_to_states.items()
        ]
