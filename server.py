from flask import Flask, render_template, request, redirect, url_for, abort, flash
from werkzeug.utils import secure_filename
from os import path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Cache age = 0
app.secret_key = b'r;l5rpKIH&7e7w0~l{*&Gjst'

################ ROUTES ################
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        usr = request.form['user']
        return redirect(f'user/{usr}')
    pf = request.user_agent.platform
    return render_template('index.html', pf=pf)
        

@app.route('/user/<name>')
def users(name=None):
    allowed_users = ['Sarah', 'Samuel', 'Daniel']
    if name not in allowed_users:
        abort(404)
    return render_template('user.html', name=name)    

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for f in files:
            f.save(path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename)))
        user = request.form['user_name']
        flash('Upload Successful')
        return redirect(f'user/{user}')
    return redirect(url_for('index'), code=302)
###################################