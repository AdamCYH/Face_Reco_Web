from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import serializers

from main.models import FaceFeature, User, MatchJob, MatchUser, Detection


class FaceFeatureSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.user_id')

    def create(self, validated_data):
        try:
            face_feature = FaceFeature.objects.create(
                user_id=validated_data['user']['user_id'],
                features=validated_data['features'])
        except IntegrityError:
            raise serializers.ValidationError("feature exists, please use PUT method to update")
        return face_feature

    def update(self, instance, validated_data):
        instance.features = validated_data.get('features', instance.features)
        instance.save()
        return instance

    def validate_user(self, value):
        try:
            User.objects.get(user_id=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("user does not exist")

        return value

    class Meta:
        model = FaceFeature
        fields = ('user', 'features')


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User.objects.create(**validated_data, enroll_time=timezone.now())

    class Meta:
        model = User
        fields = ('user_id', 'fname', 'lname', 'age', 'description', 'photo_path', 'enroll_time')
        read_only_fields = ('user_id', 'enroll_time')


class MatchUserSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.user_id')

    class Meta:
        model = MatchUser
        fields = ('user', 'confidence_level')


class MatchJobSerializer(serializers.ModelSerializer):
    match_users = MatchUserSerializer(many=True)

    # def create(self, validated_data):
    #     match_users = validated_data.pop("match_users")
    #     match_job = MatchJob.objects.get(job_id=self.context.get("job_id"))
    #     for match_user in match_users:
    #         MatchUser.objects.create(job=match_job,
    #                                  user_id=match_user['user']['user_id'],
    #                                  confidence_level=match_user['confidence_level'])
    #     return match_job

    def update(self, instance, validated_data):
        match_users = validated_data.pop("match_users")
        for match_user in match_users:
            MatchUser.objects.create(job=instance,
                                     user_id=match_user['user']['user_id'],
                                     confidence_level=match_user['confidence_level'])
        return instance

    class Meta:
        model = MatchJob
        fields = ('job_id', 'match_time', 'match_users')
        read_only_fields = ('job_id', 'match_time')


class DetectionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.user_id')

    def create(self, validated_data):
        return Detection.objects.create(
            user_id=validated_data['user']['user_id'],
            detect_camera=validated_data['detect_camera'],
            location=validated_data['location'],
            detected_photo_path=validated_data['detected_photo_path'],
            detection_time=timezone.now(),
            confidence_level=validated_data['confidence_level'])

    def validate_user(self, value):
        try:
            User.objects.get(user_id=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("user does not exist")
        return value

    class Meta:
        model = Detection
        fields = ('detection_id', 'user', 'detect_camera', 'location', 'detected_photo_path', 'detection_time',
                  'confidence_level')
        read_only_fields = ('detection_id', 'detection_time')
