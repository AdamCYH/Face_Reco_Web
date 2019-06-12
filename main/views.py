from django.http import JsonResponse
from django.shortcuts import render

from main.utilities import utilities


def recognition(request):
    if request.method == "POST":
        image_name = request.POST.get("img_name")
        image_data = request.POST.get("img_data")

        photo_path = utilities.save_image(image_name, image_data)

        # redis.push_to_redis(photo_path)

        return JsonResponse({})
    elif request.method == "GET":
        return render(request, 'main/recognition.html')


def enrollment(request):
    return render(request, 'main/enrollment.html')
