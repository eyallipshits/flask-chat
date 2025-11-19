from flask import Flask, render_template, request, Response
from datetime import datetime
from Chat_db import db  # Import the file we just made

app = Flask(__name__)

# Initialize DB on startup
with app.app_context():
    try:
        db.init_db()
        print("DB Connected!")
    except Exception as e:
        print(f"DB Connection failed (might be starting up): {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<room>")
def roomchat(room):
    return render_template("index.html")

@app.route("/api/chat/<room>", methods=["GET", "POST"])
def get_chat(room):
    if request.method == "POST":
        username = request.form.get("username", "").strip() or "Anonymous"
        msg = request.form.get("msg", "").strip()
        if not msg: return "Empty", 400
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save to MySQL via db.py
        try:
            db.insert_message(room, timestamp, username, msg)
            return "OK", 200
        except Exception as e:
            print(e)
            return "DB Error", 500
    else:
        # Read from MySQL via db.py
        try:
            messages = db.select_room(room)
            lines = [f"[{m['timestamp']}] {m['sender']}: {m['text']}" for m in messages]
            return Response("\n".join(lines), mimetype="text/plain")
        except Exception as e:
            print(e)
            return Response("DB Error", mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)