from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Demo version color (change this to "blue" or "green" for Rollout demo)
APP_COLOR = "red"  # Change to green for the next rollout version

class GuestEntry(BaseModel):
    name: str
    message: str

entries: List[GuestEntry] = []

@app.get("/", response_class=HTMLResponse)
def root():
    # Basic HTML UI for guestbook
    page = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Guestbook Demo</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: {APP_COLOR};
                color: white;
                text-align: center;
                padding-top: 50px;
            }}
            form {{
                margin: 20px auto;
                display: inline-block;
                text-align: left;
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 8px;
            }}
            input, textarea {{
                display: block;
                width: 300px;
                margin-bottom: 10px;
                padding: 8px;
                border-radius: 4px;
                border: none;
            }}
            button {{
                padding: 8px 16px;
                background-color: white;
                color: black;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }}
            button:hover {{
                background-color: lightgray;
            }}
            .entries {{
                margin-top: 40px;
            }}
        </style>
    </head>
    <body>
        <h1>Guestbook Demo ({APP_COLOR.title()} Version)</h1>
        <form method="post" action="/sign-ui">
            <input type="text" name="name" placeholder="Your Name" required>
            <textarea name="message" placeholder="Your Message" required></textarea>
            <button type="submit">Sign Guestbook</button>
        </form>

        <div class="entries">
            <h2>Guestbook Entries</h2>
            <ul>
                {"".join([f"<li>{e.name}: {e.message}</li>" for e in entries])}
            </ul>
        </div>
    </body>
    </html>
    """
    return page

@app.post("/sign-ui", response_class=HTMLResponse)
async def sign_book_ui(name: str = Form(...), message: str = Form(...)):
    entry = GuestEntry(name=name, message=message)
    entries.append(entry)
    return root()

@app.post("/sign")
def sign_book(entry: GuestEntry):
    entries.append(entry)
    return {"message": "Entry added successfully"}

@app.get("/entries", response_model=List[GuestEntry])
def list_entries():
    return entries