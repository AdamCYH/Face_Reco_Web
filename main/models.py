from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    age = models.IntegerField()
    description = models.CharField(max_length=1000)
    photo_path = models.CharField(max_length=500)
    registration_time = models.DateTimeField()

    class Meta:
        db_table = 'user'


class FaceFeatures(models.Model):
    visitor = models.OneToOneField(User, verbose_name='user_id', primary_key=True, on_delete=models.CASCADE)
    features = models.TextField()

    class Meta:
        db_table = 'face_features'


class Detection(models.Model):
    detection_id = models.AutoField(primary_key=True)
    visitor = models.ForeignKey(User, on_delete=models.CASCADE)
    detect_camera = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200)
    detected_photo_path = models.CharField(max_length=500, null=True)
    detection_time = models.DateTimeField(null=True)
    confidence_level = models.DecimalField(null=True, max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'detection'
