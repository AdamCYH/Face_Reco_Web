from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    age = models.IntegerField()
    description = models.CharField(max_length=1000)
    photo_path = models.CharField(max_length=500)
    registration_time = models.DateTimeField()
    face_feature = models.ForeignKey('FaceFeatures', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user'


class FaceFeatures(models.Model):
    visitor = models.OneToOneField(User, verbose_name='user_id', primary_key=True, on_delete=models.CASCADE)
    features = models.TextField()

    class Meta:
        db_table = 'face_features'
