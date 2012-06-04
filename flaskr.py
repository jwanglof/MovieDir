# -*- coding: utf-8 -*-
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from scan import Scanner

#Configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
FOLDERFILE = './static/folders'

#Create the application
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

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
    return render_template('scan.html', dirs=dirs, items=fscan.scanFolder(dirs), order=False)

@app.route('/desc')
def scan_desc():
    fscan = Scanner()
    dirs = fscan.getFolders(FOLDERFILE)
    return render_template('scan.html', dirs=dirs, items=fscan.scanFolder(dirs), order=True)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/folders', methods=['GET', 'POST'])
def admin_folders():
    fscan = Scanner()
    folders = fscan.getFolders(FOLDERFILE)

    if request.method == 'POST':
        if fscan.setFolders(FOLDERFILE, request.form['folders']):
            flash('Folders were successfully added')
            return redirect(url_for('scan'))
        else:
            flash('Could not write to file. Try again')
            return render_template('admin_folders.html', folders=folders)
    else:
        return render_template('admin_folders.html', folders=folders)

if __name__ == '__main__':
    app.run()



