from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from main.models import FaceFeature, User
from main.serializer import FaceFeatureSerializer, UserSerializer
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
        redis.push_to_redis(user)

        return render(request, 'main/successful.html')
    elif request.method == "GET":
        return render(request, 'main/enrollment.html')


def recognition(request):
    if request.method == "POST":
        image_name = request.POST.get("img_name")
        image_data = request.POST.get("img_data")

        photo_path = utilities.save_image(image_data, "recognition", image_name)

        # redis.push_to_redis(photo_path)

        return JsonResponse({})
    elif request.method == "GET":
        return render(request, 'main/recognition.html')


##############################
############ API #############
##############################
class FaceFeatureViewSet(viewsets.ModelViewSet):
    queryset = FaceFeature.objects.all()
    serializer_class = FaceFeatureSerializer

    # def list(self, request):
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = FaceFeature(queryset)
    #     return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def list(self, request):
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = User(queryset)
    #     return Response(serializer.data)
