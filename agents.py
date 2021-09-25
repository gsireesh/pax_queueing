import random


class Guest():

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

    def plan(self, park):
        self.next_ride = random.choice(park.attractions)
        return self.next_ride

    def log_tick(self, tick_content):
        self.history.append(tick_content)
