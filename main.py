from threading import Lock

# ...existing code...

# Global lock for thread safety
lock = Lock()

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    with lock:
        # Validate activity exists
        if activity_name not in activities:
            raise HTTPException(status_code=404, detail="Activity not found")

        # Get the specific activity
        activity = activities[activity_name]

        # Normalize email
        email = email.lower()

        # Check if the student is already signed up
        if email in activity["participants"]:
            raise HTTPException(status_code=400, detail="Student already signed up for this activity")

        # Check if the activity is full
        if len(activity["participants"]) >= activity["max_participants"]:
            raise HTTPException(status_code=400, detail="Activity is full")

        # Add student
        activity["participants"].append(email)
        
    return {"message": f"Signed up {email} for {activity_name}"}
