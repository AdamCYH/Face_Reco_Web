from rest_framework import serializers

from main.models import FaceFeature, User, MatchJob, MatchUser


class FaceFeatureSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.user_id')

    def create(self, validated_data):
        return FaceFeature.objects.create(
            user_id=validated_data['user']['user_id'],
            features=validated_data['features'])

    class Meta:
        model = FaceFeature
        fields = ('user', 'features')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'fname', 'lname', 'age', 'description', 'photo_path', 'enroll_time')
        read_only_fields = ('user_id',)


class MatchUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = MatchUser
        fields = ('confidence_level', 'user')
        ordering = ('confidence_level',)


class MatchJobSerializer(serializers.ModelSerializer):
    match_users = MatchUserSerializer(many=True, read_only=True)

    # def create(self, validated_data):
    #     match_user = validated_data.pop('user_list')
    #     job_obj = MatchJob.objects.get(job_id=validated_data['match_job'])
    #     for user in match_user:
    #         user_obj = User.objects.get(user_id=user['user_id'])
    #         conf_level = user['confidence_level']
    #         MatchUser.objects.create(match_job=job_obj, user=user_obj, confidence_level=conf_level)
    #     return job_obj

    class Meta:
        model = MatchJob
        fields = ('job_id', 'match_users')

    def validate_user(self, value):
        pass

    def validate_job(self, attrs):
        pass
