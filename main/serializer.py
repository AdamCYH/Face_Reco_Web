from rest_framework import serializers

from main.models import FaceFeature, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'fname', 'lname', 'age', 'description', 'photo_path', 'enroll_time')


class FaceFeatureSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.CharField(source='user.user_id')

    def create(self, validated_data):
        return FaceFeature.objects.create(
            user_id=validated_data['user']['user_id'],
            features=validated_data['features'])

    class Meta:
        model = FaceFeature
        fields = ('user', 'features')
