# FlaskLoginApp
---
- This project is simple implementation Login Registration flow in Flask-MySQL AND postgresql.

### Modules used
---
| Module Name    | Usage in Application |
|----------------|----------------------|
|Flask           |Web Framework to create Application|
|Flask-Login     | User Session Management in Flask|
|Flask-SQLAlchemy|Adding support of SQLAlchemy into application|
|SQLAlchemy      |Provide ORM and  full power and flexibility of SQL |
|Werkzeug        | For hashing and checking password|

### Installation
---
- Install all the dependencies using requirements.txt file...
- ```pip install -r requirements.txt```

### Running
---
##### To run Database (pass the create_app result so Flask-SQLAlchemy gets the configuration.)
- ```from project import db, create_app```
- ```db.create_all(app=create_app())```

##### Setup on Windows
- setting flask application in Windows
- ```set FLASK_APP=project```
- ```set FLASK_DEBUG=1```

##### Setup on Unix
- setting flask application in Unix
- ```export FLASK_APP=project```
- ```export FLASK_DEBUG=1```

#### Run Application
- After setting flask application, To run application use below command
- ```flask run --port=8080```
- ```--port``` is optional

# Author
---
- V A M S E E &nbsp; K R I S H N A A

# Thank You!
