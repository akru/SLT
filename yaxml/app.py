#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, make_response, request, session
from search import YaSearch 

################################################################################
##
##  Yandex - XML simple searcher.
##
################################################################################

# Configuration
DEBUG = True
SECRET_KEY = 'foo'

# Create application
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
    try:
        session['user']
        return render_template('search.html')
    except KeyError:
        return render_template('index.html')

@app.route('/search')
def search():
    try:
        req_string = request.values['req_string']

    except KeyError:
        return make_response('Bad request', 400)
    
    try:
        user = session['user']
        key = session['key']
        ya = YaSearch(user, key)
        res = ya.search(req_string)
        print user, key, req_string

        if res.error is None:
            return render_template('report.html', results=res.items)
        else:
            return render_template('report.html', error=res.error)

    except KeyError:
        return make_response('Access denied', 403)

@app.route('/auth')
def auth():
    try:
        user = request.values['user']
        key = request.values['key']
        
        resp = make_response(render_template('search.html'))
        session['user'] = user
        session['key'] = key
        return resp

    except KeyError:
        return make_response('Bad request', 400)

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('key', None)
    return render_template('logout.html')


# Self server mode
if __name__ == '__main__':
    app.run()
