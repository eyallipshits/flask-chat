from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

#Eyal: Read DB configuration from environment with sensible defaults for local dev.
MYSQL_USER = os.environ.get("MYSQL_USER", "chatuser")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "chatpass")
MYSQL_DB = os.environ.get("MYSQL_DB", "chatdb")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")

#Eyal: SQLAlchemy connection string for a MySQL database using the pymysql driver.
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
)

#Eyal: Disable the event system to save memory (not needed for this simple app).
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Eyal: Initialize the ORM
db = SQLAlchemy(app)


class Message(db.Model):
    """Denis:Represents a chat message stored in the database.

    Columns:
    - `id`: primary key
    - `room`: chat room identifier (string)
    - `username`: display name of the sender
    - `text`: message body
    - `timestamp`: when the message was created (UTC)
    """

    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


#Eyal: Ensure tables exist when the app context is available. In production you may
# want to manage migrations instead of calling `create_all()`.
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    """Eyal: Serve the main chat UI.

    The frontend (e.g. `templates/index.html`) is responsible for choosing a
    room and interacting with the `/api/chat/<room>` endpoint.
    """

    return render_template("index.html")


@app.route("/<room>")
def roomchat(room):
    """Eyal:Serve the chat UI for a specific room.

    The UI can read the room from the path and then call the API to fetch and
    post messages for that room.
    """

    return render_template("index.html")


@app.route("/api/chat/<room>", methods=["GET", "POST"])
def get_chat(room):
    """Eyal:API endpoint to fetch or post chat messages for `room`.

    POST (form data):
      - `username` (optional): sender name; defaults to "Anonymous" when empty
      - `msg` (required): message text
      Returns: 200 "OK" on success, 400 on validation error.

    GET:
      Returns a plain-text list of messages for the room, one per line,
      prefixed with a timestamp and username.
    """

    #Denis: POST -> create a new message
    if request.method == "POST":
        #Denis:Prefer a trimmed username; fall back to a default if the client sends nothing or only whitespace.
        username = request.form.get("username", "").strip() or "Anonymous"

        #Denis: Message body (required)
        msg = request.form.get("msg", "").strip()

        #Denis: Validate: don't accept empty messages
        if not msg:
            return "Empty", 400

        #Denis: Create and persist the message
        message = Message(room=room, username=username, text=msg)
        db.session.add(message)
        db.session.commit()

        return "OK", 200

    #Denis: GET -> return all messages for the room in chronological order
    messages = (
        Message.query.filter_by(room=room)
        .order_by(Message.timestamp.asc())
        .all()
    )

    if not messages:
        #Denis: Return a simple plain-text response when there are no messages yet.
        return Response("No message yet.", mimetype="text/plain")

    #Eyal: Format each message as: [YYYY-mm-dd HH:MM:SS] username: text
    lines = [
        f"[{m.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {m.username}: {m.text}"
        for m in messages
    ]

    return Response("\n".join(lines), mimetype="text/plain")


if __name__ == "__main__":
    #Eyal: Run the development server. In production use a WSGI server.
    app.run(debug=True, host='0.0.0.0', port=5000)