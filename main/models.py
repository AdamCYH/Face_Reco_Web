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
        db_table = 'users'


class FaceFeature(models.Model):
    user = models.OneToOneField(User, verbose_name='user', primary_key=True, on_delete=models.CASCADE)
    features = models.TextField()

    class Meta:
        db_table = 'face_features'


class MatchJob(models.Model):
    job_id = models.AutoField(primary_key=True)
    match_time = models.DateTimeField()
    users = models.ManyToManyField(User, through='MatchUser')

    class Meta:
        db_table = 'match_jobs'


class MatchUser(models.Model):
    job = models.ForeignKey(MatchJob, db_index=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='confidence_level', on_delete=models.CASCADE)
    confidence_level = models.DecimalField(null=True, max_digits=5, decimal_places=2)

    class Meta:
        # unique_together = ('job', 'user')
        db_table = 'match_users'
