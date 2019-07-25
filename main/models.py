from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    age = models.IntegerField(null=True)
    description = models.CharField(max_length=1000, null=True)
    photo_path = models.CharField(max_length=500)
    enroll_time = models.DateTimeField()
    vip = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = 'users'


class FaceFeature(models.Model):
    user = models.OneToOneField(User, verbose_name='user', primary_key=True, on_delete=models.CASCADE)
    features = models.TextField()

    class Meta:
        db_table = 'face_features'


class MatchJob(models.Model):
    job_id = models.AutoField(primary_key=True)
    match_time = models.DateTimeField()

    class Meta:
        db_table = 'match_jobs'


class MatchUser(models.Model):
    job = models.ForeignKey(MatchJob, related_name="match_users", db_index=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confidence_level = models.DecimalField(null=True, max_digits=23, decimal_places=20)

    class Meta:
        db_table = 'match_users'
        ordering = ['job', '-confidence_level']


class Detection(models.Model):
    detection_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    detect_camera = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    detected_photo_path = models.CharField(max_length=500, null=True)
    detection_time = models.DateTimeField(null=True)
    confidence_level = models.DecimalField(null=True, max_digits=23, decimal_places=20)

    class Meta:
        db_table = 'detections'
