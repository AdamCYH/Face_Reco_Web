from django.http import JsonResponse
from django.shortcuts import render

from main.utilities import utilities


def recognition(request):
    if request.method == "POST":
        image_name = request.POST.get("img_name")
        image_data = request.POST.get("img_data")

        photo_path = utilities.save_image(image_data, "recognition", image_name)

        # redis.push_to_redis(photo_path)

        return JsonResponse({})
    elif request.method == "GET":
        return render(request, 'main/recognition.html')


def enrollment(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        age = request.POST.get("age")
        image_data = request.POST.get("img_holder")

        photo_path = utilities.save_image(image_data, "enrollment", fname=fname, lname=lname)

        # redis.push_to_redis(photo_path)

        return render(request, 'main/successful.html')
    elif request.method == "GET":
        return render(request, 'main/enrollment.html')
