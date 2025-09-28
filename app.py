import streamlit as st
import json
# rom supabase_client import signup_user, login_user, save_trip, get_trips
from agents.planner_agent import plan_trip
# from agents.hotel_agent import get_hotel_availability   # commented for now
# from agents.weather_agent import get_weather_forecast   # commented for now

st.set_page_config(page_title="AI Trip Planner", page_icon="🌍", layout="wide")

# if "user" not in st.session_state:
    # st.session_state.user = None

st.title("🌍 AI Trip Planner Supabase")

# --- Auth Section ---
# if not st.session_state.user:
  #  choice = st.radio("Login / Signup", ["Login", "Signup"])
   # email = st.text_input("Email")
   # password = st.text_input("Password", type="password")

    #if choice == "Signup" and st.button("Signup"):
     #   if not email or not password:
      #      st.error("❌ Please enter a valid email and password.")
       # else:
        #    try:
         #       result = signup_user(email, password)
          #      if result.user:
           #         st.success("✅ Account created! Please log in now.")

            #    else:
            #        st.error("❌ Signup failed. Try a different email.")
            # except Exception as e:
            #     st.error(f"❌ Signup error: {str(e)}")

    #if choice == "Login" and st.button("Login"):
     #   if not email or not password:
      #      st.error("❌ Please enter a valid email and password.")
       # else:
        #    try:
         #       user = login_user(email, password)
          #      if user and user.user:
           #         st.session_state.user = user.user
            #        st.rerun()
             #   else:
              #      st.error("❌ Invalid credentials. Please check your email or password.")
            #except Exception as e:
             #   st.error(f"❌ Login error: {str(e)}")

#else:
 #   st.sidebar.success(f"Logged in as {st.session_state.user.email}")
  #  st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"user": None}))

    # --- Trip Planning ---
from_location = st.text_input("From (Your starting city/airport)")
destination = st.text_input("To (Destination City)")
days = st.number_input("Days", min_value=1, step=1)
interests = st.text_area("Your Interests (e.g., food, adventure, history)")
budget = st.number_input("Your Total Budget (₹)", min_value=1000, step=500)
  
if st.button("Plan My Trip"):
      # Core plan (now includes budget)
      trip_plan = plan_trip(from_location, destination, days, interests, budget)
  
      # Display results
      st.subheader("🗺️ Trip Plan (Budget-Conscious)")
      st.write(trip_plan)
  
      # Weather temporarily disabled
      # weather = get_weather_forecast(destination, str(checkin), str(checkout))
      # st.subheader("🌤️ Weather Forecast")
      # for w in weather:
      #     st.write(f"{w['date']} → {w['temp']}°C, {w['description']}")
  
      # Save trip if logged in
     # if st.session_state.user:
         # try:
        #      save_trip({
          #        "from": from_location,
           #       "to": destination,
            #      "plan": trip_plan,
             #     "budget": budget
              #})
         # except Exception as e:
          #    st.warning(f"⚠️ Could not save trip: {str(e)}")
      #else:
       #   st.info("ℹ️ Trip not saved since you are not logged in.")
  
  # --- View Past Trips ---
  #  if st.button("View Past Trips"):
  #     trips = get_trips()
  
      # Sort trips by latest first
  #     trips_sorted = sorted(trips.data, key=lambda x: x.get("id", 0), reverse=True)
  
  #   for t in trips_sorted:
  #      trip_data = t.get("trip_data")
  #     if isinstance(trip_data, str):
  #           trip_data = json.loads(trip_data)
  #           pass
  
  #    if isinstance(trip_data, dict):
  #        st.markdown(f"**📍 {trip_data.get('from', '')} → {trip_data.get('to', '')}**")
  #        st.write(f"💰 Budget: ₹{trip_data.get('budget', 'N/A')}")
  #        st.write(trip_data.get("plan", "No plan found"))
  #    else:
  #        st.write(trip_data)
