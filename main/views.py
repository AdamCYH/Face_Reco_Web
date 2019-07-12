import json
import logging
import time

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status, generics
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import FaceFeature, User, MatchJob, MatchUser, Detection
from main.serializer import FaceFeatureSerializer, UserSerializer, MatchJobSerializer, DetectionSerializer, \
    DetectionReadSerializer, FaceFeatureReadSerializer, MatchJobReadSerializer
from main.utilities import utilities, redis, sql

logger = logging.getLogger(__name__)


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
            logger.error(user_serializer.errors)

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
        photo_path = utilities.save_image(image_data, "recognition", img_name=image_name)

        # create a new recognition job
        match_job = sql.create_job()

        # send new recognition job id and photo path to redis for SDK recognition
        redis.recognition_redis(photo_path, match_job.job_id)

        # try to get recognition result, if not continue trying
        match_result = ""
        # break if exceed 2 mins
        timeout = time.time() + 30
        while match_result == "":
            if time.time() > timeout:
                return JsonResponse({"data": "Service is busy, please try again later."})
            match_result = redis.result_from_redis(match_job.job_id)
            time.sleep(1)

        # insert recognition result to database
        match_job = sql.insert_match_result(match_result)

        serializer = MatchJobReadSerializer(match_job)
        data = json.loads(str(JSONRenderer().render(serializer.data), encoding="utf8"))
        return JsonResponse({"data": data})


class LiveView(View):
    # get request, return the template
    def get(self, request):
        return render(request, 'main/live.html')


class FaceFeatureViewSet(viewsets.ViewSet):
    """
    This view is the REST api view for face feature creation, retrieving, updating, and listing
    """

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
            logger.error(serializer.errors)

        return Response(serializer.data)


class UserViewSet(viewsets.ViewSet):
    """
    This view is the REST api view for user creation, retrieving, and listing
    """

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
            logger.error(serializer.errors)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class MatchJobViewSet(viewsets.ViewSet):
    """
    This view is the REST api view for matchjob updating, retrieving, and listing
    Since server creates the matchjob when user submit request, so the view does not provide
    CREATE api
    """

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

    def update(self, request, pk=None):
        exist_jobs = MatchUser.objects.filter(job_id=pk)
        exist_jobs.delete()

        queryset = MatchJob.objects.get(job_id=pk)
        serializer = self.serializer_class(queryset, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            logger.error(serializer.errors)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DetectionViewSet(viewsets.ViewSet):
    """
    This view is the REST api view for detection creation, retrieving, and listing
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DetectionViewSet, self).dispatch(request, *args, **kwargs)

    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer
    read_serializer_class = DetectionReadSerializer

    def list(self, request):
        queryset = Detection.objects.all()
        serializer = self.read_serializer_class(queryset, many=True)
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


class DetectionStatus(generics.ListAPIView):
    serializer_class = DetectionReadSerializer

    def get_queryset(self):
        try:
            initial_call = self.request.GET.get('initial_call')
            last_entry = self.request.GET.get('last_entry')
            num_entries = self.request.GET.get('num_entries')

            if initial_call.lower() == "true":
                return Detection.objects.all().order_by('-detection_id')[:int(num_entries)]
            else:
                return Detection.objects.filter(detection_id__gt=int(last_entry)).order_by('-detection_id')
        except AttributeError:
            raise APIException("Invalid Parameters")


class LoadFeatures(APIView):
    def get(self, request, format=None):
        """
        Load face feature to Redis, so SDK can use for recognition
        """
        queryset = FaceFeature.objects.all()
        users = FaceFeatureReadSerializer(queryset, many=True)
        redis.load_feature_to_redis(users.data)
        return Response({"Status": "Successful"}, status=status.HTTP_200_OK)
