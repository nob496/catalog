#Access and test your application by visiting
 http://localhost:8000

#Information about python scripts.
 application.py: main file.
 database_setup.py: creates hikingtrailinfo.db with SQLAlchemy.
 hikingtrails.py: adds hiking trail info to the DB.

#Information about the database.
 Database: sqlite, hikingtrailinfo.db (run database_setup.py & hikingtrails.py to create)
 Tables: user/hiking/trail_info

#Python version.
 Python 2.7.12 (pip install python 2.7)

#Important Packages which you should import to run the script.
 flask (http://flask.pocoo.org/): API to create Web app with Python script.
 sqlalchemy, sqlalchemy.orm (https://www.sqlalchemy.org/): python SQL toolkit and Object Relational Mapper.
 oauth2client (https://oauth2client.readthedocs.io/en/latest/): makes it easy to interact with OAuth2-protected resources.
 json (https://docs.python.org/3/library/json.html): creates JSON endpoints for this app.
 requests (https://2.python-requests.org//en/master/): the only Non-GMO HTTP library for Python.
 httplib2 (https://pypi.org/project/httplib2/): a comprehensive HTTP client library.

#/templates
 login.html(/login): login page (with google or facebook account)
 header.html: header for hikingDays.html/trailInfo.html to login/logout
 hikingDays.html(/hikingDays/): main page (park information)
  -newPark.html(/hikingDays/new/): creates new park infomation
  -editPark.html(/hikingDays/<int:park_id>/edit/): edits park information
  -deletePark.html(/hikingDays/<int:park_id>/delete/): deletes park information
  -trailInfo.html(/hikingDays/<int:park_id>): trail information
   --newTrailInfo.html(/hikingDays/<int:park_id>/new/): creates new trail information
   --editTrailInfo.html(/hikingDays/<int:park_id>/<int:id>/edit): edits trail information
   --deleteTrail.html(/hikingDays/<int:park_id>/<int:id>/delete): deletes trail information

#/static
 styles.css: style sheet for all the html files

#What this web app does?
This is hiking records. We can create/edit/delete park information/trail information.
