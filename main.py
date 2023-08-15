from flask import Flask
import json
import datetime


app = Flask(__name__)

@app.route('/')
def home():
	return "Homepage"

@app.route('/<string:username>')
def user(username):
	return f"{username}`s page"

@app.route('/threads')
def threads():
	return "Threads page"

@app.route('/thread/<string:treadname>')
def thread(threadname):
	return f"{threadname} page"

@app.route('/login')
def login():
	return "login page"

@app.route('/signin')
def signin():
	return "sign in page"


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080)