from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets

from main.models import FaceFeature, User, MatchJob
from main.serializer import FaceFeatureSerializer, UserSerializer, MatchJobSerializer
from main.utilities import utilities, redis, sql


##############################
######### SITE VIEW ##########
##############################
def enrollment(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        age = request.POST.get("age")
        description = request.POST.get("description")
        image_data = request.POST.get("img_holder")

        photo_path = utilities.save_image(image_data, "enrollment", fname=fname, lname=lname)

        user = sql.insert_visitor(fname, lname, age, description, photo_path)
        redis.enroll_to_redis(user)

        return render(request, 'main/successful.html')
    elif request.method == "GET":
        return render(request, 'main/enrollment.html')


def recognition(request):
    if request.method == "POST":
        image_name = request.POST.get("img_name")
        image_data = request.POST.get("img_data")

        photo_path = utilities.save_image(image_data, "recognition", image_name)

        match_job = sql.create_job()

        match_result = ""
        while match_result == "":
            match_result = redis.recognition_redis(photo_path, match_job.job_id)

        sql.insert_match_result(match_result)
        return JsonResponse({})
    elif request.method == "GET":
        return render(request, 'main/recognition.html')


##############################
############ API #############
##############################
class FaceFeatureViewSet(viewsets.ModelViewSet):
    queryset = FaceFeature.objects.all()
    serializer_class = FaceFeatureSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MatchJobViewSet(viewsets.ModelViewSet):
    queryset = MatchJob.objects.all()
    serializer_class = MatchJobSerializer
