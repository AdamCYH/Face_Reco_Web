from django.utils import timezone

from main.models import User


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
