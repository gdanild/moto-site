from flask import redirect, render_template, request
from web import app
from web.forms import AddPostForm
import socket,time, random, requests, json



#====================================================================
#====================================================================
#====================================================================




@app.route('/', methods=['GET', 'POST'])
def main():
    form = AddPostForm(csrf_enabled=False)
    return render_template('main.html', form=form, error_login=False)

@app.route('/square', methods=['GET', 'POST'])
def square():
    form = AddPostForm(csrf_enabled=False)
    return render_template('square.html', form=form, error_login=False)
