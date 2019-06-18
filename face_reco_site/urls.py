"""face_reco_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import EnrollmentView, RecognitionView, FaceFeatureViewSet, UserViewSet, MatchJobViewSet

router = DefaultRouter()
router.register(r'face_feature', FaceFeatureViewSet)
router.register(r'user', UserViewSet)
router.register(r'match_job', MatchJobViewSet)

urlpatterns = [
    path('', EnrollmentView.as_view()),
    path('api/', include(router.urls)),
    path('recognition', RecognitionView.as_view(), name='main-recognition_site'),
    path('enrollment', EnrollmentView.as_view(), name='main-enrollment_site'),

]
