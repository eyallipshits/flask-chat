from flask import Flask,redirect,url_for,render_template, request, Response
import os

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/<room>")
def roomchat(room):
    return render_template("index.html")

@app.route("/api/chat/<room>", methods=["GET"])
def get_chat(room):
    room_file = os.path.join(DATA_DIR, f"{room}.txt")

    if not os.path.exists(room_file):
        return Response("No message yet.", mimetype="text/plain")
    
    lines = []
    with open(room_file, "r", encoding="utf-8") as f:
        for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = [p.strip() for p in line.split("|", 2)]
                if len(parts) != 3:
                     continue
                
                timestamp, username, msg = parts
                formatted = f"[{timestamp}] {username}: {msg}"
                lines.append(formatted)

    final_text = "\n".join(lines)
    return Response(final_text, mimetype="text/plain")

if __name__ == '__main__':
    app.run(debug=True)