import json
import os

import redis

POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
my_server = redis.Redis(connection_pool=POOL)

TASK_NULL = 0
TASK_CREATE_USER = 1
TASK_DELETE_USER = 2
TASK_LOAD_USERS = 3
TASK_FACE_REGISTRATION = 101


def push_to_redis(u_id, fname, lname, photo_path):
    # Create user and save it into redis db
    user_info = {
        'id': int(u_id),
        'name': '%s %s' % (fname, lname),
        'photo_path': os.path.abspath(photo_path)
    }
    my_server.set('FR_user:_%d' % u_id, json.dumps(user_info))

    task_info = {
        'task_id': TASK_FACE_REGISTRATION,
        'user_id': int(u_id)
    }
    my_server.publish('test-channel', json.dumps(task_info))

    # new thread to get feature from sdk and insert to SQL
    # download_thread = Thread(target=get_face_feature, args=(u_id,))
    # download_thread.setDaemon(True)
    # download_thread.start()
    return 1


# load feature from SQL database to redis, so SDK can extract face feature again.
def load_feature_to_redis(users):
    for v_id, user in users.items():
        # Create user and save it into redis db
        user_info = {
            'id': int(v_id),
            'name': '%s %s' % (user.fname, user.lname),
            'photo_path': os.path.abspath(user.photo_path),
            'feature': user.face_feature.features
        }
        my_server.set('user:%d' % v_id, json.dumps(user_info))

        task_info = {
            'task_id': TASK_LOAD_USERS,
            'user_id': int(v_id)
        }
        my_server.publish('test-channel', json.dumps(task_info))
