from django.utils import timezone

from main.models import User, MatchJob, MatchUser


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
        match_user = MatchUser()
        match_user.job = match_job
        match_user.user = User.objects.get(user_id=user["user_id"])
        match_user.confidence_level = user["confidence_level"]
        match_user.save()

    return match_job
