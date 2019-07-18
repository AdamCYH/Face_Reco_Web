import logging

from django.utils import timezone

from main.models import User, MatchJob, MatchUser

logger = logging.getLogger(__name__)


def insert_visitor(fname, lname, age, description, photo_path):
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
    match_job = MatchJob()
    match_job.match_time = timezone.now()
    match_job.save()
    return match_job


def insert_match_result(match_result):
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
