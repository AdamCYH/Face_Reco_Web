from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    age = models.IntegerField(null=True)
    description = models.CharField(max_length=1000, null=True)
    photo_path = models.CharField(max_length=500)
    enroll_time = models.DateTimeField()

    class Meta:
        db_table = 'user'


class FaceFeature(models.Model):
    user = models.OneToOneField(User, verbose_name='user', primary_key=True, on_delete=models.CASCADE)
    features = models.TextField()

    class Meta:
        db_table = 'face_feature'


class MatchResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    result_content = models.CharField(max_length=2000)

    class Meta:
        db_table = 'match_result'
