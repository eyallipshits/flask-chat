from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

MYSQL_USER = os.environ.get("MYSQL_USER", "chatuser")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "chatpass")
MYSQL_DB = os.environ.get("MYSQL_DB", "chatdb")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

with app.app_context():
    db.create_all()

# Go to the home page
@app.route("/")
def home():
    return render_template("index.html")


# go to a some room chat
@app.route("/<room>")
def roomchat(room):
    return render_template("index.html")

@app.route("/api/chat/<room>", methods=["GET", "POST"])
def get_chat(room):
    if request.method == "POST":
        # get from the user username
        username = request.form.get("username", "").strip() or "Anonymous"
        # get from the user the message
        msg = request.form.get("msg", "").strip()

        if not msg:
            return "Empty message ignored", 400
        
        message = Message(room=room, username=username, text=msg)
        db.session.add(message)
        db.session.commit()

        return "OK", 200
    
    messages = Message.query.filter_by(room=room).order_by(Message.timestamp.asc()).all()

    if  not messages:
        return Response("No message yet.", mimetype="text/plain")
    
    lines = [
        f"[{m.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {m.username}: {m.text}"
        for m in messages
    ]
        
    return Response("\n".join(lines), mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)
