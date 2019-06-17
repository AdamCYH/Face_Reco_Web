from django.http import JsonResponse
from django.shortcuts import render

from main.utilities import utilities, redis, sql


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
