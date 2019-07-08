import json
import time

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from main.models import FaceFeature, User, MatchJob, MatchUser, Detection
from main.serializer import FaceFeatureSerializer, UserSerializer, MatchJobSerializer, DetectionSerializer
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

        # user = sql.insert_visitor(fname, lname, age, description, photo_path)
        if age == "":
            age = None
        if description == "":
            description = None
        data = {
            'fname': fname,
            'lname': lname,
            'age': age,
            'description': description,
            'photo_path': photo_path,
            'enroll_time': timezone.now()
        }

        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
        else:
            print(user_serializer.errors)

        if user is not None:
            redis.enroll_to_redis(user)
            return render(request, 'main/successful.html')
        else:
            return render(request, 'main/enrollment.html')


# view for recognition
class RecognitionView(View):
    # get request, return the template
    def get(self, request):
        return render(request, 'main/recognition.html')

    # process recognition pipeline
    def post(self, request):
        image_name = request.POST.get("img_name")
        image_data = request.POST.get("img_data")

        # save uploaded image
        photo_path = utilities.save_image(image_data, "recognition", image_name)

        # create a new recognition job
        match_job = sql.create_job()

        # send new recognition job id and photo path to redis for SDK recognition
        redis.recognition_redis(photo_path, match_job.job_id)

        # try to get recognition result, if not continue trying
        match_result = ""
        while match_result == "":
            match_result = redis.result_from_redis(match_job.job_id)

        # insert recognition result to database
        match_job = sql.insert_match_result(match_result)

        serializer = MatchJobSerializer(match_job)
        data = json.loads(str(JSONRenderer().render(serializer.data), encoding="utf8"))
        time.sleep(3)
        # data = {"job_id": 23, "match_users": [{"confidence_level": "97.80",
        #                                        "user": {"user_id": 1, "fname": "Adam", "lname": "Chiu", "age": 25,
        #                                                 "description": "Research Assistant at CyLab",
        #                                                 "photo_path": "./media/photos/enrollment/Adam_Chiu_201906211406.png",
        #                                                 "enroll_time": "2019-06-18T17:41:36.664004Z"}},
        #                                       {"confidence_level": "87.60",
        #                                        "user": {"user_id": 2, "fname": "Bob", "lname": "Bil", "age": 25,
        #                                                 "description": "test",
        #                                                 "photo_path": "./media/photos/enrollment/Adam_Chiu_201906241814.png",
        #                                                 "enroll_time": "2019-06-18T17:41:59.236418Z"}},
        #                                       {"confidence_level": "76.90",
        #                                        "user": {"user_id": 3, "fname": "user3", "lname": "adam", "age": 29,
        #                                                 "description": "Hello My Name is adam\r\nthis is the second line\r\nthis is the second line\r\nthis is the second line\r\nthis is the second line\r\nthis is the second line\r\nthis is the second line\r\n",
        #                                                 "photo_path": "./media/photos/enrollment/bob__201906131900.png",
        #                                                 "enroll_time": "2019-06-18T18:43:56.896219Z"}}]}
        # data = {"job_id": 23, "match_users": []}

        return JsonResponse({"data": data})


class LiveView(View):
    # get request, return the template
    def get(self, request):
        return render(request, 'main/live.html')


class FaceFeatureViewSet(viewsets.ViewSet):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(FaceFeatureViewSet, self).dispatch(request, *args, **kwargs)

    queryset = FaceFeature.objects.all()
    serializer_class = FaceFeatureSerializer

    def list(self, request):
        queryset = FaceFeature.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        queryset = FaceFeature.objects.all()
        feature = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(feature)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = FaceFeature.objects.get(user_id=pk)
        serializer = self.serializer_class(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            print(serializer.errors)

        return Response(serializer.data)


class UserViewSet(viewsets.ViewSet):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserViewSet, self).dispatch(request, *args, **kwargs)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        queryset = User.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            print(serializer.errors)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class MatchJobViewSet(viewsets.ViewSet):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(MatchJobViewSet, self).dispatch(request, *args, **kwargs)

    queryset = MatchJob.objects.all()
    serializer_class = MatchJobSerializer

    def list(self, request):
        queryset = MatchJob.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = MatchJob.objects.all()
        feature = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(feature)
        return Response(serializer.data)

    # def update(self, request, pk=None):
    #     #     job_id = pk
    #     #     exist_jobs = MatchUser.objects.filter(job_id=job_id)
    #     #     exist_jobs.delete()
    #     #
    #     #     serializer = self.serializer_class(data=request.data, context={'job_id': job_id})
    #     #     if serializer.is_valid(raise_exception=True):
    #     #         serializer.save()
    #     #     else:
    #     #         print(serializer.errors)
    #     #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        exist_jobs = MatchUser.objects.filter(job_id=pk)
        exist_jobs.delete()

        queryset = MatchJob.objects.get(job_id=pk)
        serializer = self.serializer_class(queryset, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            print(serializer.errors)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DetectionViewSet(viewsets.ViewSet):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DetectionViewSet, self).dispatch(request, *args, **kwargs)

    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer

    def list(self, request):
        queryset = Detection.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        queryset = Detection.objects.all()
        feature = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(feature)
        return Response(serializer.data)
