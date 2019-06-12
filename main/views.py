from django.http import JsonResponse
from django.shortcuts import render

from main.utilities import utilities, redis


# Create your views here.
def home(request):
    return render(request, 'main/recognition.html')


def detection(request):
    image_name = request.POST.get("img_name")
    image_data = request.POST.get("img_data")

    photo_path = utilities.save_image(image_name, image_data)

    # redis.push_to_redis(photo_path)

    return JsonResponse({})
