from flask import Flask, render_template, request, redirect, url_for, abort, flash
from werkzeug.utils import secure_filename
from math import floor
from os import path, scandir

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

@app.route('/user/<name>/view') # Get user name var in. Use in render at end.
def image_view(name):
    # Dynamic generation of responsive image grid - Maybe fixed size grid still auto generate? or hardcode
    cols = 4
    rows = 4
    html_card = '<div class="row">\n'
    count = 0
    done = False
    directory = 'C:\\Users\\Sam\\Documents\\Uni\\Python\\website\\uploads\\'
    file_names = [file for file in scandir(directory)]
    if file_names == None:
        return 'Error' # Call render with error var

    for i in range(cols):
        if done:
            break
        html_card += '<div class="column">\n'
        for i in range(rows):
            try:
                fn = 'test/' + file_names[count].name 
                # 'test' is the directory that is sym linked to the dir of images
                src = url_for('static', filename=fn)
                html_card += f'<img src="{src}">\n'
                count += 1
            except:
                done = True
        html_card += '</div>\n'
    html_card += '</div>\n'
    html_card
    return render_template('view.html', html_card=html_card)
###################################