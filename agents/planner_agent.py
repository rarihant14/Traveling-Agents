import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from ddgs import DDGS   

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def search_train(from_city, to_city):
    query = f"{from_city} to {to_city} train ticket price site:irctc.co.in"
    with DDGS() as ddgs:
        results = ddgs.text(
            query,
            region="in-en",
            safesearch="Moderate",
            timelimit="d"
        )
        return [r["title"] + " - " + r["body"] for r in results]

def search_flight(from_city, to_city):
    query = f"{from_city} to {to_city} flight ticket price"
    with DDGS() as ddgs:
        results = ddgs.text(
            query,
            region="in-en",
            safesearch="Moderate",
            timelimit="d"
        )
        return [r["title"] + " - " + r["body"] for r in results]

def plan_trip(from_location, destination, days, interests, budget):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)

    train_info = search_train(from_location, destination)
    flight_info = search_flight(from_location, destination)

    train_text = "\n".join(train_info[:3]) if train_info else "No live train info found."
    flight_text = "\n".join(flight_info[:3]) if flight_info else "No live flight info found."

    prompt = f"""
    You are an experienced travel planner with a sense of humor. 
    Plan a {days}-day trip from {from_location} to {destination}.

    The user is interested in {interests}.
    The user's total budget is ₹{budget}. Make sure your plan stays within this budget.
    
    ### Travel Options (Live Data Included)
    🚆 Train (latest info):
    {train_text}

    ✈️ Flight (latest info):
    {flight_text}

    ### Instructions for Output:
    1. Choose the best travel option (flight/train) under budget.
    2. Provide a structured day-wise itinerary that fits within the budget.
    3. Suggest affordable dining and activities based on the user's interests.
    4. Add puns, jokes, or light humor.
    5. VERY IMPORTANT: If {destination} is unsafe, warn the user: "⚠️ Not safe to visit now."
    6. If the budget is too low, warn: "⚠️ Budget may not be enough. Adjust expectations."
    
    Format with:
    - Travel Options
    - Day-wise Itinerary
    - Dining & Activities
    - Safety Advice
    - Budget Note
    """

    response = llm.invoke(prompt)
    return response.content
