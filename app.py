from flask import Flask,redirect,url_for,render_template, request, Response
from datetime import datetime
import os

app = Flask(__name__)

#DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

rooms = {}

# Go to the home page
@app.route("/")
def home():
    return render_template("index.html")


# go to a some room chat
@app.route("/<room>")
def roomchat(room):
    return render_template("index.html")

@app.route("/api/chat/<room>", methods=["GET","POST"])
def get_chat(room):

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

            # create a message dictionary
            messages = {"timestamp": datetime.now(),"sender": username, "text": msg}

            # put that list to that specific room
            rooms[room].append(messages)
            
            return "Every thing is ok"

    if request.method == "GET":

        if room not in rooms :
            return Response("No message yet.", mimetype="text/plain")
            
            #lines = []
            output=[]
        for mesg in rooms[room]:
            
                mesg['timestamp']
                    
        #final_text = "\n".join(rooms[room])
        return Response(final_text, mimetype="text/plain")
    

if __name__ == "__main__":
    app.run(debug=True)
