from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import serializers

from main.models import FaceFeature, User, MatchJob, MatchUser


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
        user = User(**validated_data)
        user.enroll_time = timezone.now()
        return user

    class Meta:
        model = User
        fields = ('user_id', 'fname', 'lname', 'age', 'description', 'photo_path', 'enroll_time')
        read_only_fields = ('user_id', 'enroll_time')


class MatchUserSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.user_id')

    def create(self, validated_data):
        try:
            match_user = MatchUser.objects.create(
                job_id=self.context.get("job_id"),
                confidence_level=validated_data['confidence_level'],
                user_id=validated_data['user']['user_id'])
        except IntegrityError:
            raise serializers.ValidationError("job or user not found")
        return match_user

    class Meta:
        model = MatchUser
        fields = ('user', 'confidence_level')
        ordering = ('confidence_level',)


class MatchJobSerializer(serializers.ModelSerializer):
    match_users = MatchUserSerializer(many=True, read_only=True)

    class Meta:
        model = MatchJob
        fields = ('job_id', 'match_time', 'match_users')
        read_only_fields = ('job_id', 'match_time')
