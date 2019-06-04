#!/usr/bin/env python

'''
Created the web application about trail information for hiking.
Please read README.txt for the detailed information.
'''

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Hiking, TrailInfo, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Hiking Record Application"

engine = create_engine('sqlite:///hikingtrailinfo.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/login')
def showLogin():
    #  Create Anti-Forgery State Token.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

#  Login with facebook account.
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/oauth/access_token?grant_type='
           + 'fb_exchange_token&client_id='
           + '%s&client_secret=%s&fb_exchange_token=%s'
           % (app_id, app_secret, access_token))
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    #  Use token to get user info from API.
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange
        we have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then
        we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that
        it can be used directly in the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = ('https://graph.facebook.com/v2.8/me?access_token'
           + '=%s&fields=name,id,email'
           % token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    #  The token must be stored in the login_session
    #  in order to properly logout.
    login_session['access_token'] = token

    #  Get user picture.
    url = ('https://graph.facebook.com/v2.8/me/picture?access_token'
           + '=%s&redirect=0&height=200&width=200'
           % token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    #  See if user exists.
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    #  output += ' " style = "width: 300px; height: 300px;border-radius: 150px;
    #  -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("Now logged in as %s" % login_session['username'])
    return output

#  Logout of facebook.
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    #  The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = ('https://graph.facebook.com/%s/permissions?access_token=%s'
           % (facebook_id, access_token))
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

#  login with google account.
@app.route('/gconnect', methods=['POST'])
def gconnect():
    #  Validate state token.
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #  Obtain authorization code.
    code = request.data

    try:
        #  Upgrade the authorization code into a credentials object.
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #  Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    #  If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #  Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                   json.dumps('Current user is already connected.'),
                   200)
        response.headers['Content-Type'] = 'application/json'
        return response

    #  Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    #  Get user info.
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    #  ADD PROVIDER TO LOGIN SESSION.
    login_session['provider'] = 'google'

    #  See if user exists, if it doesn't make a new one.
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    #  output += ' " style = "width: 300px; height: 300px;border-radius: 150px;
    #  -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


#  User Helper Functions
def createUser(login_session):
    '''Creates a new user in the database.
    Args:
       login_session: session object with user data.
    Returns:
       user.id: generated distinct integer value identifying the newly created
    '''
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    '''Get the user information in the database.
    Args:
       user_id (in user table, id)
    Returns:
       user (attr: name, email, picture)
    '''
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    '''Get the user ID in the database.
    Args:
       email
    Returns:
       user.id (if it exists)
    '''
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None

#  Logout of google.
@app.route('/gdisconnect')
def gdisconnect():
    #  Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/hikingDays/JSON')
def parkInfoJSON():
    '''JSON APIs to view Park Information.
    Returns:
       all parks information
    '''
    parks = session.query(Hiking).all()
    return jsonify(parks=[r.serialize for r in parks])


@app.route('/hikingDays/<int:park_id>/JSON')
def trailInfoJSON(park_id):
    '''List all trails info with JSON format.
    Args:
       park_id (in trail_info table, Column(Integer, ForeignKey('hiking.id')))
    Returns:
       all trails information having the park_id.
    '''
    trails = session.query(TrailInfo).filter_by(park_id=park_id).all()
    return jsonify(trails=[i.serialize for i in trails])


@app.route('/hikingDays/')
def hikingDays():
    '''List all the parks info in the database.
    Returns:
       hikingDays.html with parks (all the parks information)
    '''
    parks = session.query(Hiking).order_by(asc(Hiking.park))
    return render_template('hikingDays.html', parks=parks)


@app.route('/hikingDays/new/', methods=['GET', 'POST'])
def newPark():
    '''Create new park info.
    Returns:
       on GET: page to create a new park info.
       on POST: Redirected to main page after Item has been created.
                Empty post is not allowed.
                See if the new park name already exists.
       Login page when user is not signed in.
    '''
    if 'username' not in login_session:
        return redirect('/login')
    parks = session.query(Hiking).all()
    allParks = []
    for i in parks:
        allParks.append(i.park)
    if request.method == 'POST':
        if request.form['name'] == '':
            flash('Invalid Request! Empty post is not allowed.')
            return redirect(url_for('hikingDays'))
        #  See if the park that the user inputted is already in the list.
        if request.form['name'] in allParks:
            flash('Already exists!')
            return redirect(url_for('hikingDays'))
        else:
            newPark = Hiking(park=request.form['name'],
                             user_id=login_session['user_id'])
            session.add(newPark)
            flash('New Park %s Successfully Created' % newPark.park)
            session.commit()
            return redirect(url_for('hikingDays'))
    else:
        return render_template('newPark.html')


@app.route('/hikingDays/<int:park_id>/edit/', methods=['GET', 'POST'])
def editPark(park_id):
    '''Edit park info.
    Args:
       park_id (in trail_info table, Column(Integer, ForeignKey('hiking.id')))
    Returns:
       on GET: page to edit the park info.
       on POST: Redirected to main page after Item has been edited.
                Empty post is not allowed.
                Check for User Authorization (Permission).
       Login page when user is not signed in.
    '''
    if 'username' not in login_session:
        return redirect('/login')
    editedPark = session.query(Hiking).filter_by(id=park_id).one()
    if editedPark.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this park inforamtion.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedPark.park = request.form['name']
            session.add(editedPark)
            flash('Park Successfully Edited %s' % editedPark.park)
            session.commit()
            return redirect(url_for('hikingDays'))
    else:
        return render_template('editPark.html', park=editedPark)


@app.route('/hikingDays/<int:park_id>/delete/', methods=['GET', 'POST'])
def deletePark(park_id):
    '''Delete park info.
    Args:
       park_id (in trail_info table, Column(Integer, ForeignKey('hiking.id')))
    Returns:
       on GET: page to edit the park info.
       on POST: Redirected to main page after Item has been deleted.
                Check for User Authorization (Permission).
       Login page when user is not signed in.
    '''
    if 'username' not in login_session:
        return redirect('/login')
    parkToDelete = session.query(Hiking).filter_by(id=park_id).one()
    if parkToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this park inforamtion.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(parkToDelete)
        flash('%s Successfully Deleted' % parkToDelete.park)
        session.commit()
        return redirect(url_for('hikingDays'))
    else:
        return render_template('deletePark.html', park=parkToDelete)


@app.route('/hikingDays/<int:park_id>')
def trailInfo(park_id):
    '''Trail information, list all the trails information in the park.
    Args:
       park_id (in trail_info table, Column(Integer, ForeignKey('hiking.id')))
    Returns:
       trailInfo.html with park and trails (all the trails information in the park)
    '''
    park = session.query(Hiking).filter_by(id=park_id).one()
    trails = session.query(TrailInfo).filter_by(park_id=park_id)
    return render_template('trailInfo.html', park=park, trails=trails)


@app.route('/hikingDays/<int:park_id>/new/', methods=['GET', 'POST'])
def newTrailInfo(park_id):
    '''Create new trail information.
    Args:
       park_id (in trail_info table, Column(Integer, ForeignKey('hiking.id')))
    Returns:
       on GET: page to create a new trail info.
       on POST: Redirected to trails info in the park page after Item has been created.
                Empty post for trail is not allowed.
                See if the new trail name already exists.
       Login page when user is not signed in.
    '''
    if 'username' not in login_session:
        return redirect('/login')
    park = session.query(Hiking).filter_by(id=park_id).one()
    trails = session.query(TrailInfo).filter_by(park_id=park_id)
    allTrails = []
    for i in trails:
        allTrails.append(i.trail)
    if request.method == 'POST':
        if request.form['trail'] == '':
            flash('Invalid Request! Empty post is not allowed.')
            return redirect(url_for('trailInfo', park_id=park.id))
        #  See if the trail that the user inputted is already in the list.
        if request.form['trail'] in allTrails:
            flash('Already exists!')
            return redirect(url_for('trailInfo', park_id=park.id))
        else:
            newTrail = TrailInfo(trail=request.form['trail'], park_id=park_id,
                                 user_id=login_session['user_id'])
            if request.form['date']:
                newTrail.date = request.form['date']
            if request.form['url']:
                newTrail.url = request.form['url']
            if request.form['address']:
                newTrail.address = request.form['address']
            if request.form['distance']:
                newTrail.distance = request.form['distance']
            if request.form['elevation']:
                newTrail.elevation = request.form['elevation']
            if request.form['level']:
                newTrail.level = request.form['level']
                session.add(newTrail)
                flash('New Trail %s Successfully Created' % newTrail.trail)
                session.commit()
                return redirect(url_for('trailInfo', park_id=park.id))
    else:
        return render_template('newTrailInfo.html', park=park)


@app.route('/hikingDays/<int:park_id>/<int:id>/edit', methods=['GET', 'POST'])
def editTrailInfo(park_id, id):
    '''Edit trail information.
    Args:
       park_id (in trail_info table, Column(Integer, ForeignKey('hiking.id')))
       id (in trail_info table, trail id)
    Returns:
       on GET: page to edit the trail info.
       on POST: Redirected to trails info in the park page after Item has been edited.
                Empty post for trail is not allowed.
                Check for User Authorization (Permission).
       Login page when user is not signed in.
    '''
    if 'username' not in login_session:
        return redirect('/login')
    park = session.query(Hiking).filter_by(id=park_id).one()
    editedTrail = session.query(TrailInfo).filter_by(id=id).one()
    if editedTrail.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this trail inforamtion.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['trail']:
            editedTrail.trail = request.form['trail']
        if request.form['date']:
            editedTrail.date = request.form['date']
        if request.form['url']:
            editedTrail.url = request.form['url']
        if request.form['address']:
            editedTrail.address = request.form['address']
        if request.form['distance']:
            editedTrail.distance = request.form['distance']
        if request.form['elevation']:
            editedTrail.elevation = request.form['elevation']
        if request.form['level']:
            editedTrail.level = request.form['level']
        session.add(editedTrail)
        session.commit()
        flash('Trail Successfully Edited')
        return redirect(url_for('trailInfo', park_id=park.id))
    else:
        return render_template('editTrailInfo.html', trail=editedTrail)


@app.route('/hikingDays/<int:park_id>/<int:id>/delete',
           methods=['GET', 'POST'])
def deleteTrailInfo(park_id, id):
    '''Delete trail information.
    Args:
       park_id (in trail_info table, Column(Integer, ForeignKey('hiking.id')))
       id (in trail_info table, trail id)
    Returns:
       on GET: page to delete the trail info.
       on POST: Redirected to trails info in the park page after Item has been deleted.
                Check for User Authorization (Permission).
       Login page when user is not signed in.
    '''
    if 'username' not in login_session:
        return redirect('/login')
    park = session.query(Hiking).filter_by(id=park_id).one()
    trailToDelete = session.query(TrailInfo).filter_by(id=id).one()
    if trailToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this trail inforamtion.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(trailToDelete)
        flash('%s Successfully Deleted' % trailToDelete.trail)
        session.commit()
        return redirect(url_for('trailInfo', park_id=park.id))
    else:
        return render_template('deleteTrail.html', trail=trailToDelete)

#  Disconnect based on provider.
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('hikingDays'))
    else:
        flash("You were not logged in")
        return redirect(url_for('hikingDays'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
