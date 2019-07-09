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
TASK_FACE_LOAD = 103


def enroll_to_redis(user):
    """
    Enrollment function. it put user info into redis, and publish a task into channel for application to
    process face feature extraction
    """
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
    """
    Recognition function. Publish recognition task to the channel for face recognition.
    """
    task_info = {
        'task_id': TASK_FACE_RECOGNITION,
        'photo_path': os.path.abspath(photo_path),
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
    """
    Feature loading function. extract face feature from persistent db, put into redis and publish load task to the channel
    for application to read feature data for incoming recognition.
    """
    for user in users:
        user_id = int(user['user']['user_id'])
        # Create user and save it into redis db
        user_info = {
            'id': user_id,
            'name': '%s %s' % (user['user']['fname'], user['user']['lname']),
            'photo_path': os.path.abspath(user['user']['photo_path']),
            'feature': user['features']
        }
        print('FR:%d' % user_id, user_info)
        my_server.set('FR:%d' % user_id, json.dumps(user_info))

        task_info = {
            'task_id': TASK_FACE_LOAD,
            'user_id': user_id
        }
        print(task_info)
        my_server.publish('load-channel', json.dumps(task_info))
