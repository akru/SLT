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
        return render_template('search.html', user=session['user'])

    except KeyError:
        return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        qfile = request.files['qfile']

    except KeyError:
        return make_response('Bad request', 400)
    
    try:
        user = session['user']
        key = session['key']
        ya = YaSearch(user, key)

        results = {}
        for qstring in qfile:
            if len(qstring) > 1:
                res = ya.search(qstring)

                if res.error is None:
                    results[qstring] = res.items
                else:
                    print res.error.code, res.error.description
                    return render_template('report.html', error=res.error, user=user)

        return render_template('report.html', results=results, user=user)

    except KeyError:
        return make_response('Access denied', 403)

@app.route('/auth')
def auth():
    try:
        user = request.values['user']
        key = request.values['key']
        
        session['user'] = user
        session['key'] = key
        return render_template('search.html', user=user)

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
