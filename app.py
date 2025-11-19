from flask import Flask, redirect, url_for, render_template, request, session
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


@app.route("/api/chat/<room>", methods=["POST"])
def api_chat_room(room):

    if request.method == "POST":

        # get from the user username
        username = request.form["username"]

        # get from the user the message
        msg = request.form["msg"]

        # if the room is not exists, create and store in dictionary
        if room not in rooms:
            rooms[room] = []

            # if the room exists
            if room in rooms:

                # create a message list
                messages = {"sender": username, "text": msg, "timestamp": datetime.now()}

                # put that list to that specific room
                rooms[room].append(messages)

                return "Every thing is ok"


if __name__ == "__main__":
    app.run(debug=True)
