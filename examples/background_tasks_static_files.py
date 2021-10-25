from fastapi import BackgroundTasks, FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

def process_background_notification(email: str, message=""):
    with open("task_logs.txt", mode="w") as log_file:
        contents = f"notification for {email}: {message}"
        # maybe perform send notification
        log_file.write(contents)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_background_notification, email, message="notifying")
    return {"message": "Notification being processed."}

app.mount("/public", StaticFiles(directory="public"), name="static")
