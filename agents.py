import random
from collections import defaultdict

from constants import STATE_WAITING, STATE_RIDING


def _run_length_encode(l):
    last_item = ""
    current_count = 0
    rle_list = []
    for item in l:
        if item == last_item:
            current_count += 1
        else:
            rle_list.append((last_item, current_count))
            current_count = 1
            last_item = item
    else:
        rle_list.append((last_item, current_count))
    return rle_list[1:]


class Guest:
    def __init__(self, name: str, preferences=None):
        self.name = name
        self.preferences = preferences
        self.last_ride = None
        self.next_ride = None
        self.history = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def get_day_log(self):
        rle_log = _run_length_encode(self.history)
        return "\n".join(
            [f"Spent {item[1]} ticks {item[0][1]} at {item[0][0].lower()}" for item in rle_log]
        )

    def get_day_breakdown(self):
        activity_to_time_map = defaultdict(lambda: 0)
        for activity_log in self.history:
            if activity_log[1] == STATE_WAITING:
                activity_to_time_map[STATE_WAITING] += 1
            else:
                activity_to_time_map[STATE_RIDING] += 1
        return activity_to_time_map

    def get_day_breakdown_string(self):
        activity_to_time_map = self.get_day_breakdown()
        return f"Spent {activity_to_time_map[STATE_WAITING]} ticks waiting and in between rides, and {activity_to_time_map[STATE_RIDING]} ticks on rides"

    def plan(self, park):
        self.next_ride = random.choice(park.attractions)
        return self.next_ride

    def log_tick(self, tick_content):
        self.history.append(tick_content)


class FixedItineraryGuest(Guest):
    def __init__(self, name, itinerary, p_random_choice=0.05):
        super().__init__(name=name)
        self.itinerary_mutable = itinerary.copy()
        self.itinerary = itinerary
        self.p_random_choice = p_random_choice

    def plan(self, park):
        if self.itinerary_mutable and random.random() > self.p_random_choice:
            self.next_ride = self.itinerary_mutable.pop()
            return self.next_ride
        else:
            super().plan(park)


class QueueLengthGuest(Guest):
    def __init__(self, name):
        super().__init__(name=name)

    def plan(self, park):
        min_queue_length = 1e10
        next_ride = None
        for ride in park.attractions:
            if len(ride.queue) < min_queue_length:
                min_queue_length = len(ride.queue)
                next_ride = ride
        self.next_ride = next_ride
        return self.next_ride
