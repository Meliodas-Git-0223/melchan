from flask import Flask, render_template, redirect, request, url_for, flash
import json, os
import datetime,random,asyncio
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user


app = Flask(__name__)
app.secret_key = 'qaswedfrtghyu'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_id, name, password):
        self.id = user_id
        self.name = name
        self.password = password

with open('data/users.json', 'r') as f:
	users_data = json.load(f)
	users = {user['id']: User(user['id'], user['name'], user['password']) for user in users_data['users']}
	f.close()

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))


@app.route('/')
def home():
	return "Homepage"

@app.route('/user/<string:username>')
@login_required
def user(username):
	return f"{username}`s page"


@app.route("/newmessage", methods=["POST"])
def getdata():
	name = request.form.get("name")
	message = request.form.get("message")
	return "get"


@app.route('/threads/<string:username>')
@login_required
def threads(username):
	print(users.get(1))
	thrs = []
	thrnames = []
	for c in os.listdir('data/threads'):
		thrs.append(c)
		thrnames.append(c.split('.')[0])
	return render_template('threads.html', threads = thrs, threadnames = thrnames, username = username)




@app.route('/thread/<string:username>/<string:threadname>')
@login_required
def thread(threadname,username):
	messages = {}
	with open(f'data/threads/{threadname}.json', 'r') as f:
		data = json.load(f)
		for d in data['messages']:
			messages[d["name"]] = d['text']

	return render_template('thread.html', messages = messages, thread = threadname, username = username)




@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		name = request.form['name']
		password = request.form['password']
		with open('data/users.json') as f:
			data = json.load(f)
			for d in data['users']:
				print(d)
				if d['name'] == name:
					r = d['id']
					break
			f.close()
		user_id = int(r)
		user = users.get(user_id)
		if user and user.password == password:
			login_user(user)
			return redirect(url_for('threads'))
	return render_template('login.html', username = 'login')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	global users
	if request.method == 'POST':
		name = request.form['name']
		password = request.form['password']
		user_id = random.randint(0,646116)
		with open('data/users.json', 'r') as f:
			data = json.load(f)
			print(f"id: {user_id}, name: {name}, password: {password}")
			tname = []
			tid = []
			for d in data['users']:
				tid.append(d['id'])
				tname.append(d['name'])
			
			f.close()
			
			if user_id in tid:
				while user_id in tid:
					user_id = random.randint(0,646116)
			
			print(data)
			print(tid)
			print(tname)
			
			if user_id not in tid:
				if name not in tname:
					data['users'].append({"id": user_id, 'name': name, 'password': password})
					print(data)
					with open('data/users.json', 'w') as df:
						df.write(json.dumps(data, indent=4))
						df.close()
					with open('data/users.json', 'r') as f:
						users_data = json.load(f)
						users = {user['id']: User(user['id'], user['name'], user['password']) for user in users_data['users']}
						f.close()

					redirect('/login')
			
	
	with open('data/users.json', 'r') as f:
			data = json.load(f)
			tname = []
			for d in data['users']:
				tname.append(d['name'])
	
	tnames = ''

	for i in range(len(tname) - 1):
		tnames += f",{tname[i+1]}"

	tnames = tname[0] + tnames
					
	return render_template('signin.html', tname = tnames)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "Logged out successfully."


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080)