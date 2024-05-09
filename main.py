from flask import Flask, render_template, redirect, request, url_for
import json, os, hashlib
import random
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
from packages import b64

UPLOAD_FOLDER = 'static/media/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp', 'mp3', 'gif', 'webm', 'mp4', 'ogg', 'avi', 'bmp', 'wav'])
images = ['png', 'jpg', 'jpeg', 'webp', 'bmp', 'gif']
videos = ['webm', 'mp4','ogg', 'avi']
audio = [ 'mp3', 'wav']

app = Flask(__name__)
app.secret_key = 'wert7iyujhgfdesw345'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





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
	threads = os.listdir('data/threads')
	rantr = random.choice(threads)
	return render_template('home.html', username = 'login', rantr = rantr.split(".")[0])

@app.route('/user/<string:username>')
@login_required
def user(username):
	return f"{username}`s page"


@app.route("/newmessage", methods=["POST"])
@login_required
def getdatamedia():
	name = request.form.get("name")
	cur = datetime.now()
	date = f"{cur.day}.{cur.month}.{cur.year}, {cur.hour}:{cur.minute}:{cur.second}"
	tfile = request.form.get('tfile')
	if tfile == "true":
		file = request.files['file']
		if file.filename.split(".")[1] in videos:
			media = 'video'
		elif file.filename.split(".")[1] in images:
			media = 'image'
		elif file.filename.split(".")[1] in audio:
			media = 'audio'

		print(file.filename.split(".")[1])
		

		if file and allowed_file(file.filename):
			filename = secure_filename(b64.encode(f"{cur.day}.{cur.month}.{cur.year}, {cur.hour}:{cur.minute}:{cur.second}:{cur.microsecond}") + "."+ file.filename.split(".")[1])
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	
	if tfile =='false':
		media = None
		filename = None

	threadname = request.form.get("threadname")
	message = request.form.get("message")
	messageid = int(f"{cur.day}{cur.month}{cur.year}{cur.hour}{cur.minute}{cur.second}{cur.microsecond}")
	print("get " + message + " from " + name + " in thread " + threadname)
	
	with open(f'data/threads/{threadname}.json', 'r') as f:
		data = json.load(f)
		f.close()
		
	
	with open(f'data/threads/{threadname}.json', 'w') as f:
		data['messages'].append({'name': name,'date':date, 'text': message, 'id':messageid, 'media':media, 'media-filename':filename})
		f.write(json.dumps(data, indent=4))
		f.close()
	return 'get', 200



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/threads')
@login_required
def threads():
	print(current_user.name)
	thrs = []
	thrnames = []
	for c in os.listdir('data/threads'):
		thrs.append(c)
		thrnames.append(c.split('.')[0])
	return render_template('threads.html', threads = thrs, threadnames = thrnames, username = current_user.name)

@app.route('/threadsadmin')
@login_required
def threadsadmin():
	print(current_user.name)
	thrs = []
	thrnames = []
	for c in os.listdir('data/threads'):
		thrs.append(c)
		thrnames.append(c.split('.')[0])
	return render_template('threadsadmin.html', threads = thrs, threadnames = thrnames, username = current_user.name)

@app.route('/threads/create')
@login_required
def create_thr():
	return render_template("create_thr.html", username = current_user.name)

@app.route('/newthread', methods = ["POST"])
@login_required
def new_thread():
	name = current_user.name
	id = random.randint(0,646116)
	cur = datetime.now()
	date = f"{cur.day}.{cur.month}.{cur.year}, {cur.hour}:{cur.minute}:{cur.second}"
	threadname = request.form.get('thrname')
	d = "{" + f''' "name": "{name}","date":"{date}", "id":{id}, "messages": [] ''' + "}"
	print(threadname)
	print(name)
	with open(f'data/threads/{threadname}.json', 'x') as f:
		f.close()

	with open(f'data/threads/{threadname}.json', 'wt') as df:
		print(d)
		df.write(str(d))
		df.close()
			
	redirect(f'thread/{threadname}')

	return 'done'

@app.route('/thread/<string:threadname>')
@login_required
def thread(threadname):
	messages = {}
	with open(f'data/threads/{threadname}.json', 'r') as f:
		data = json.load(f)
		messages = data['messages']
		date = data['date']
		f.close()
	print(messages)

	return render_template('thread.html',date = date, messages = messages, thread = threadname, username = current_user.name)


@app.route('/threadadmin/<string:threadname>')
@login_required
def threadadmin(threadname):
	messages = {}
	with open(f'data/threads/{threadname}.json', 'r') as f:
		data = json.load(f)
		messages = data['messages']
		f.close()
	print(messages)

	return render_template('threadadmin.html', messages = messages, thread = threadname, username = current_user.name)






















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
		hash_object = hashlib.sha256(f'{password}'.encode('utf-8'))
		password_hash = hash_object.hexdigest()
		if user and user.password == password_hash:
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

					hash_object = hashlib.sha256(f'{password}'.encode('utf-8'))
					password_hash = hash_object.hexdigest()

					data['users'].append({"id": user_id, 'name': name, 'password': password_hash})
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
















@app.route('/delete/message/<string:threadname>/<string:messageid>')
@login_required
def delete_message(threadname,messageid):
	with open('data/admins.json') as a:
		dat = json.load(a)
	if current_user.name in dat['admins']:
		with open(f'data/threads/{threadname}.json', 'r') as f:
			data = json.load(f)
			f.close()

		for el in data['messages']:
			if el['id'] == int(messageid):
				if el['media-filename']:
					os.remove('static/media/'+el['media-filename'])
				data['messages'].remove(el)

		with open(f'data/threads/{threadname}.json', 'w') as f:
			f.write(json.dumps(data, indent=4))
			f.close()
		
		return "removed successfully."
	else:
		return 'you are not Admin. Fuck you.'


@app.route('/delete/thread/<string:threadname>')
@login_required
def delete_thread(threadname):
	with open('data/admins.json') as a:
		dat = json.load(a)
	if current_user.name in dat['admins']:
		os.remove(f'data/threads/{threadname}.json')
		

		return "removed successfully."
	else:
		return 'you are not Admin. Fuck you.'



if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080)