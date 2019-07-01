import json
import os

import redis

POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
my_server = redis.Redis(connection_pool=POOL)

TASK_NULL = 0
TASK_CREATE_USER = 1
TASK_DELETE_USER = 2
TASK_LOAD_USERS = 3

# For face recognition project
TASK_FACE_ENROLLMENT = 101
TASK_FACE_RECOGNITION = 102


def enroll_to_redis(user):
    # Create user and save it into redis db
    user_info = {
        'id': user.user_id,
        'name': '%s %s' % (user.fname, user.lname),
        'photo_path': os.path.abspath(user.photo_path)
    }
    my_server.set('FR:%d' % user.user_id, json.dumps(user_info))

    task_info = {
        'task_id': TASK_FACE_ENROLLMENT,
        'user_id': user.user_id,
    }
    my_server.publish('enroll-channel', json.dumps(task_info))

    return 1


def recognition_redis(photo_path, job_id):
    task_info = {
        'task_id': TASK_FACE_RECOGNITION,
        'photo_path': photo_path,
        'job_id': job_id
    }
    my_server.publish('recognition-channel', json.dumps(task_info))
    return 1


def result_from_redis(job_id):
    result_string = my_server.get("FR_result:%d" % job_id)
    if result_string is None:
        return ""
    result = json.loads(str(result_string, encoding='utf8'))
    return result


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
