import logging

from django.utils import timezone

from main.models import User, MatchJob, MatchUser

logger = logging.getLogger(__name__)


def insert_visitor(fname, lname, age, description, photo_path):
    """
    Depreciated. Please use serializer to insert visitors.
    :param fname: user first name
    :param lname: user last name
    :param age: user age
    :param description: user description
    :param photo_path: photo path
    :return: user object
    """
    user = User()
    user.fname = fname
    if age != "":
        user.age = age
    user.lname = lname
    user.description = description
    user.photo_path = photo_path
    user.enroll_time = timezone.now()
    user.save()
    return user


def create_job():
    """
    It creates an empty job, which is used for SDK callback to update the match result.
    :return: an empty match_job object
    """
    match_job = MatchJob()
    match_job.match_time = timezone.now()
    match_job.save()
    return match_job


def insert_match_result(match_result):
    """
    When SDK callback, it inserted match result to the database.
    :param match_result: match result
    :return: match result object
    """
    match_job = MatchJob.objects.get(job_id=match_result["job_id"])
    for user in match_result["users"]:
        try:
            match_user = MatchUser()
            match_user.job = match_job
            match_user.user = User.objects.get(user_id=user["user_id"])
            match_user.confidence_level = user["confidence_level"]
            match_user.save()
        except User.DoesNotExist:
            logger.error(":::::[Warning] Matched user {} no longer in the database.".format(user["user_id"]))
            continue

    return match_job
