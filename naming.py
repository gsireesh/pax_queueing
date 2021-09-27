import random
import string

names = [
    "Tomas",
    "Marylou",
    "Rodolfo",
    "Edgar",
    "Stuart",
    "Saul",
    "Elwood",
    "Jayne",
    "Maureen",
    "Edmundo",
    "Broderick",
    "Marion",
    "Silvia",
    "Marcie",
    "Edith",
    "Jaime",
    "Juliet",
    "Karla",
    "Shelby",
    "Shelley",
]

rollercoaster_names = [
    "Lightning Inferno",
    "Afterburner",
    "Starstrike",
    "Wild Lasso",
    "Thunderbird",
    "Skyrider"
]


def get_person_name():
    return random.choice(names) + " " + random.choice(string.ascii_uppercase)


def get_rollercoaster_names(n=1):
    if n > len(rollercoaster_names):
        raise NotImplementedError("We don't have that many rollercoaster names!")
    return rollercoaster_names[:n]
