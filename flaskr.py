# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from scan import Scanner

#Configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
FOLDERFILE = './static/folders'

#Create the application
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    """Creates the database tables."""
    with closing(connect_db()) as db:
	with app.open_resource('schema.sql') as f:
	    db.cursor().executescript(f.read())
	db.commit()

@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
	g.db.close()

        #@app.route('/')
#def show_entries():
    #cur = g.db.execute('select title, text from entries order by id desc')
    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    #return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
	abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
	if request.form['username'] != app.config['USERNAME']:
	    error = 'Invalid username'
	elif request.form['password'] != app.config['PASSWORD']:
	    error = 'Invalid password'
	else:
	    session['logged_in'] = True
	    flash('You were logged in')
	    return redirect(url_for('scan'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('scan'))

@app.route('/')
def scan():
    fscan = Scanner()
    #dirs = ['/home/johan/Downloads', '/home/johan/Downloads']
    dirs = fscan.getFolders(FOLDERFILE)
    return render_template('scan.html', dirs=dirs, items=fscan.scanFolder(dirs))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/folders', methods=['GET', 'POST'])
def admin_folders():
    fscan = Scanner()
    folders = fscan.getFolders(FOLDERFILE)

    if request.method == 'POST':
        if fscan.setFolders(FOLDERFILE, request.form['folders']):
            return redirect(url_for('scan'))
        else:
            flash('Could not write to file. Try again')
            return render_template('admin_folders.html', folders=folders)
    else:
        return render_template('admin_folders.html', folders=folders)

if __name__ == '__main__':
    init_db()
    app.run()



