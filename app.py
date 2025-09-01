import streamlit as st
import json
from supabase_client import signup_user, login_user, save_trip, get_trips
from agents.planner_agent import plan_trip
# from agents.hotel_agent import get_hotel_availability


st.set_page_config(page_title="AI Trip Planner", page_icon="🌍", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

st.title("🌍 AI Trip Planner Supabase")

# --- Auth Section ---
if not st.session_state.user:
    choice = st.radio("Login / Signup", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Signup" and st.button("Signup"):
        signup_user(email, password)
        st.success("Account created!make sure to check E-mail box, Before Please log in .")

    if choice == "Login" and st.button("Login"):
        user = login_user(email, password)
        if user.user:
            st.session_state.user = user.user
            st.rerun()
        else:
            st.error("Invalid credentials")

else:
    st.sidebar.success(f"Logged in as {st.session_state.user.email}")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"user": None}))

    # --- Trip Planning ---
    from_location = st.text_input("From (Your starting city/airport)")
    destination = st.text_input("To (Destination City)")
    days = st.number_input("Days", min_value=1, step=1)
    interests = st.text_area("Your Interests (e.g., food, adventure, history)")
    checkin = st.date_input("Check-in date")
    checkout = st.date_input("Check-out date")

    if st.button("Plan My Trip"):
        trip_plan = plan_trip(from_location, destination, days, interests)
       #  hotels = get_hotel_availability(destination, checkin, checkout)

        st.subheader("🗺️ Trip Plan")
        st.write(trip_plan)

        # st.subheader("🏨 Available Hotels")

       #  if isinstance(hotels, list):
             #if hotels:
              #  for h in hotels:
               #     if isinstance(h, dict):
                #        name = h.get("name", "Unknown")
                 #       price = h.get("price", "N/A")
                  #      rating = h.get("rating", "N/A")
                   #     st.write(f"**{name}** - {price} - ⭐ {rating}")
                    #else:
                     #   st.write(h)
            #else:3
             #   st.write("No hotels found.")
        #elif isinstance(hotels, dict):
        #    st.write(hotels.get("error", "Unexpected response format"))
        #else:
         #   st.write("No hotels found or invalid response.")

        save_trip({
            "from": from_location,
            "to": destination,
            "plan": trip_plan
        })

    # --- View Past Trips ---
    if st.button("View Past Trips"):
        trips = get_trips(st.session_state.user.id)
        for t in trips.data:
            trip_data = t.get("trip_data")
            if isinstance(trip_data, str):
                try:
                    trip_data = json.loads(trip_data)
                except:
                    pass
            if isinstance(trip_data, dict):
                st.markdown(f"**📍 {trip_data.get('from', '')} → {trip_data.get('to', '')}**")
                st.write(trip_data.get("plan", "No plan found"))
            else:
                st.write(trip_data)
