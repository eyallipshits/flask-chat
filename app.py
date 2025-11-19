from flask import Flask,redirect,url_for,render_template, request, Response
from datetime import datetime

app = Flask(__name__)

rooms = {}

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
        
        if room not in rooms:
            rooms[room] = []
        
        message = {
            "sender": username,
            "text": msg,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        rooms[room].append(message)
        return "OK", 200
    else:
        if room not in rooms or not rooms[room]:
            return Response("No message yet.", mimetype="text/plain")
    
        lines = []
        for msg in rooms[room]:
            formatted = f"[{msg['timestamp']}] {msg['sender']}: {msg['text']}"
            lines.append(formatted)

    final_text = "\n".join(lines)
    return Response(final_text, mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)
