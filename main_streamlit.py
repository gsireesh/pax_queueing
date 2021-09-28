from time import sleep

import pandas as pd
import plotly.express as px
import streamlit as st

from agents import Guest, QueueLengthGuest
from naming import get_person_name
from park_fixtures import Park
from predefs import get_attractions_1, get_itinerary_guests

## define sidebar section for real parameters
st.sidebar.write("Park Settings:")
param_form = st.sidebar.form("param_form")
n_random_riders = param_form.slider(
    "Number of Park Guests (Random Strategy)", min_value=1, max_value=1000
)
n_queue_length_riders = param_form.slider(
    "Number of Park Guests (Queue length Strategy)", min_value=0, max_value=1000
)
n_itinerary_riders = param_form.slider(
    "Number of Park Guests (Itinerary Strategy", min_value=0, max_value=1000
)
n_ticks = param_form.slider("Number of ticks over a day", min_value=10, max_value=144)
display_sim = param_form.checkbox("Display simulation?")
time_between_ticks = param_form.slider(
    "Time in between ticks (ms)", min_value=50, max_value=1000, step=50
)
submitted = param_form.form_submit_button("Re-run with new parameters")


attractions = get_attractions_1()
park = Park(attractions)

## Ride popularity settings

# popularities = []
# for attraction in attractions:
#     attraction_slider = param_form.slider(
#         f"Relative popularity for the {attraction.name}", min_value=0.0, max_value=10.0, step=0.05
#     )
#     popularities.append(attraction_slider)


random_guests = [Guest(get_person_name(), None) for i in range(n_random_riders)]
queue_length_guests = [QueueLengthGuest(get_person_name()) for i in range(n_queue_length_riders)]
itinerary_guests = get_itinerary_guests(n_itinerary_riders, attractions)

guests = random_guests + queue_length_guests + itinerary_guests

for guest in guests:
    park.accept_guest(guest)


st.title("Theme Park Queueing Simulator")
with st.expander("Park Setup", expanded=True):
    st.header("Park Setup")
    st.markdown("There are four rides at this park:")
    for a in attractions:
        st.markdown(
            f"**{a.name}**: this ride seats {a.capacity}, and takes {a.duration_ticks} ticks to ride."
        )

if display_sim:
    st.header("Park Simulation")
    with st.empty():
        for i in range(n_ticks):
            park.tick()
            park_state = pd.DataFrame(park.get_state())
            st.line_chart(pd.DataFrame(park_state))

            if display_sim:
                sleep(time_between_ticks / 1000)
else:
    for i in range(n_ticks):
        park.tick()


st.header("Guest Experiences by Type")
type_to_df_map = park.get_guest_stats_by_type()
for guest_type, guest_df in type_to_df_map.items():
    fig = px.histogram(guest_df, x=["Waiting", "Riding"], marginal="rug")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Wait/Ride time distribution for riders of type {guest_type}")
for line in park.get_guest_report():
    st.markdown(line)
