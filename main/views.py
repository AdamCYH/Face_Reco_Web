import time

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets

from main.models import FaceFeature, User, MatchJob
from main.serializer import FaceFeatureSerializer, UserSerializer, MatchJobSerializer
from main.utilities import utilities, redis, sql


# View for enrollment
class EnrollmentView(View):
    # get request, return the template
    def get(self, request):
        return render(request, 'main/enrollment.html')

    # post request, save post data into db as new user
    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        age = request.POST.get("age")
        description = request.POST.get("description")
        image_data = request.POST.get("img_holder")

        photo_path = utilities.save_image(image_data, "enrollment", fname=fname, lname=lname)

        user = sql.insert_visitor(fname, lname, age, description, photo_path)
        redis.enroll_to_redis(user)

        return render(request, 'main/successful.html')


# view for recognition
class RecognitionView(View):
    # get request, return the template
    def get(self, request):
        return render(request, 'main/recognition.html')

    # process recognition pipeline
    def post(self, request):
        # image_name = request.POST.get("img_name")
        # image_data = request.POST.get("img_data")
        #
        # # save uploaded image
        # photo_path = utilities.save_image(image_data, "recognition", image_name)
        #
        # # create a new recognition job
        # match_job = sql.create_job()
        #
        # # send new recognition job id and photo path to redis for SDK recognition
        # redis.recognition_redis(photo_path, match_job.job_id)
        #
        # # try to get recognition result, if not continue trying
        # match_result = ""
        # while match_result == "":
        #     match_result = redis.result_from_redis(match_job.job_id)
        #
        # # insert recognition result to database
        # match_job = sql.insert_match_result(match_result)
        #
        # serializer = MatchJobSerializer(match_job)
        # data = json.loads(str(JSONRenderer().render(serializer.data), encoding="utf8"))
        time.sleep(10)
        data = {"job_id": 23, "match_users": [{"confidence_level": "97.80",
                                               "user": {"user_id": 1, "fname": "Adam", "lname": "Chiu", "age": 25,
                                                        "description": "Research Assistant at CyLab",
                                                        "photo_path": "./media/photos/enrollment/Adam_Chiu_201906211406.png",
                                                        "enroll_time": "2019-06-18T17:41:36.664004Z"}},
                                              {"confidence_level": "87.60",
                                               "user": {"user_id": 2, "fname": "Bob", "lname": "Bil", "age": 25,
                                                        "description": "test",
                                                        "photo_path": "./media/photos/enrollment/Adam_Chiu_201906241814.png",
                                                        "enroll_time": "2019-06-18T17:41:59.236418Z"}},
                                              {"confidence_level": "76.90",
                                               "user": {"user_id": 3, "fname": "user3", "lname": "adam", "age": 29,
                                                        "description": "Hello My Name is adam\r\nthis is the second line\r\nthis is the second line\r\nthis is the second line\r\nthis is the second line\r\nthis is the second line\r\nthis is the second line\r\n",
                                                        "photo_path": "./media/photos/enrollment/bob__201906131900.png",
                                                        "enroll_time": "2019-06-18T18:43:56.896219Z"}}]}
        # data = {"job_id": 23, "match_users": []}

        return JsonResponse({"data": data})


class LiveView(View):
    # get request, return the template
    def get(self, request):
        return render(request, 'main/live.html')


class FaceFeatureViewSet(viewsets.ModelViewSet):
    queryset = FaceFeature.objects.all()
    serializer_class = FaceFeatureSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MatchJobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MatchJob.objects.all()
    serializer_class = MatchJobSerializer
