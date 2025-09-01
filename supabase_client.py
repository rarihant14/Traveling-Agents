import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- Auth ---
def signup_user(email, password):
    return supabase.auth.sign_up({"email": email, "password": password})


def login_user(email, password):
    return supabase.auth.sign_in_with_password({"email": email, "password": password})


def get_current_user():
    """Return currently logged-in user (if any)."""
    return supabase.auth.get_user()


# --- Trips ---
def save_trip(trip_data: dict):
    """
    Save trip for currently logged-in user.
    trip_data must be a dict (will be stored as JSONB).
    """
    user = get_current_user()
    if not user or not user.user:
        raise Exception("No logged-in user found")

    user_id = user.user.id
    return supabase.table("trips").insert({
        "user_id": user_id,
        "trip_data": trip_data
    }).execute()


def get_trips():
    """
    Get all trips for the currently logged-in user.
    """
    user = get_current_user()
    if not user or not user.user:
        raise Exception("No logged-in user found")

    user_id = user.user.id
    return supabase.table("trips").select("*").eq("user_id", user_id).execute()

