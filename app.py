from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit
import pymongo
import json
#from bson.json_util import dumps

app = Flask( __name__ )
app.secret_key = 'secret!271'
socketio = SocketIO( app )

__mongo_client = pymongo.MongoClient( 'localhost:27017', connect=False )
__mongo_database = __mongo_client['sentry-test']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_projects')
def get_projects():
    projects = {
        'projects' : list( __mongo_database['project'].find() )
    }

    for p in projects['projects']:
        p.update({
            '_id' : str( p['_id'] ),
            'created' : str( p['created'] )
        })

    
    return json.dumps(projects), 200, {'Access-Control-Allow-Origin' : '*'}


@app.route('/get_activities')
def get_activities():
    activities = {
        'activities' : list( __mongo_database['activity'].find() )
    }

    for p in activities['activities']:
        p.update({
            '_id' : str( p['_id'] ),
            'datetime' : str( p['datetime'] )
        })

    
    return json.dumps(activities), 200, {'Access-Control-Allow-Origin' : '*'}


@app.route('/add_project', methods=['POST'])
def add_project():
    __mongo_database['project'].insert_one(request.data['project'])
    return {'success' : True}

# @socketio.on('connect')
# def connect():
#     print('connection established')

# @socketio.on('/create-project')
# def create_project( payload ):
#     emit('received')


    

    
if __name__ == '__main__':
    # projects = {
    #     'data' : __mongo_database['project'].find()
    # }
    # print(projects)
    socketio.run(app, debug=True)
    
