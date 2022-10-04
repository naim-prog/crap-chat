from flask import Flask, redirect, request, render_template, url_for
import secrets
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)

# Home page
@app.route("/")
def home():
    return render_template("home.html")

# Create a room
@app.route("/create/", methods=['GET'])
def create():
    number = secrets.token_urlsafe(128)
    new_file_room = open(f"room.{number}.txt", "w")
    new_file_room.write("")
    new_file_room.close()
    return redirect(f"/room/{number}")

# GET the join.html or POST to join a room
@app.route("/join/", methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template("join-get.html")
    if request.method == 'POST':
        return redirect(f"/room/{request.form.get('room_key')}")

# Get the messages from the room
@app.get("/room/<string:number>/")
def room_get(number):
    if os.path.isfile(f"{os.getcwd()}/room.{number}.txt"):
        content_mes = open(f"room.{number}.txt", "r", encoding='utf-8').read()
        title = f"{number[:6]}...{number[-6:]}"
        msg_list = content_mes.split('\n') if content_mes else None
        return render_template("room.html", title=title, msg_list=msg_list, room_key=number)
    else:
        return "no existe esa sala"

# Post a message on the room
@app.post("/room/<string:number>/")
def room_post(number):
    content_room = open(f"room.{number}.txt", "a", encoding='utf-8')
    if request.form['message']:
        time_msg = f"[{time.localtime().tm_hour}:{time.localtime().tm_min}.{time.localtime().tm_sec}]"
        content_room.write(f"{time_msg} - {request.form['message']}\n")
    return redirect(url_for("room_get", number=number))

if __name__ == "__main__":
    os.chdir(os.getcwd())
    app.run(host="0.0.0.0", port=80, debug=True)
