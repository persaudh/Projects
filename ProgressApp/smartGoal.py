from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
import datetime
import os
from dotenv import load_dotenv
import json


# Initialize FastAPI app
app = FastAPI(title="SMART Goal Planner API")

class GoalRequest(BaseModel):
    goal: str

@app.get("/")
def read_root():
    return {"message": "SMART Goal Planner API is running."}

def get_API_key(print_key: bool = False) -> str:
    # Load environment variables from .env file
    load_dotenv()

    # Access the API key
    api_key = os.getenv("OPENAI_API_KEY")
    if print_key:
        print(f"API Key: {api_key}")

    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
    return api_key


def generate_smart_goal_plan(user_goal: str) -> dict:
    today = datetime.date.today()
    today_str = today.strftime("%B %d, %Y")

    system_prompt = f"""
    You are an expert goal-setting assistant.
    When a user provides a goal, break it down into a SMART plan using JSON format.

    SMART stands for:
    - Specific: Clearly state the goal.
    - Measurable: Define how success is measured.
    - Achievable: Ensure the goal is realistic.
    - Relevant: Explain why this goal matters.
    - Time-bound: Provide deadlines.

    Respond with a JSON object using this format:

    {{
    "goal_summary": {{
        "specific": "...",
        "measurable": "...",
        "achievable": "...",
        "relevant": "...",
        "time_bound": "...",
        "start_date": "{today_str}"
    }},
    "task_plan": [
        {{
        "task": "...",
        "due_date": "Month DD, YYYY",
        "description": "...",
        "milestone": true | false
        }},
        ...
    ]
    }}

    Use realistic deadlines and specific calendar dates based on today's date ({today_str}).
    Ensure the goal and all tasks align with the SMART framework.
    Only return the JSON. No commentary.
    Only return raw JSON without any markdown code blocks, comments, or explanations.
    """

    user_prompt = (
        f"I want to achieve the following goal: \"{user_goal}\". "
        "Please help me break this down into a SMART action plan with realistic timelines and checkpoints."
    )

    try:
       # Set your OpenAI API key
        print(os.environ.get(""))
        client = OpenAI(
        
        api_key = get_API_key(True)  # or replace with your actual key
        )
        # You can also set the base URL if you're using a different endpoint)

        response = client.responses.create(
            model="gpt-4o",
            instructions=system_prompt,
            input=user_prompt,
        )
    
        json_text = response.output_text

        # Parse JSON (with error fallback if needed)
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            print("⚠️ Warning: Could not parse JSON directly. Here is the raw output:\n")
            print(json_text)
            return {}
    
    except Exception as e:
        return f"An error occurred: {e}"
    
@app.post("/generate_plan")
def generate_plan(request: GoalRequest):
    plan = generate_smart_goal_plan(request.goal)

    # ❌ BAD (string)
    # return str(plan)

    # ✅ GOOD
    return JSONResponse(content=plan)

def main():
    print("🎯 SMART Goal Planner (JSON Format)")
    print("-----------------------------------")
    goal = input("Enter your goal: ").strip()

    if not goal:
        print("You must enter a goal to continue.")
        return

    print("\nGenerating SMART goal plan...\n")
    result = generate_smart_goal_plan(goal)

    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Failed to generate goal plan.")

if __name__ == "__main__":
    main()
