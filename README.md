This the front-end service only that includes three modules
Single image upload,
Single image recognition,
Live video recognition


## Install dependency ##

```
$ sudo apt-get install mysql-server \
    mysql-client-core-5.7 \
    libmysqlclient-dev \
    virtualenv \
    uwsgi-plugin-python
```

```
$ virtualenv airport-envs -p python3
$ source airport-envs/bin/activate

$ pip install django
$ pip install redis
$ pip install mysqlclient # use 1.3.14 if python version is 3.4 or below
$ pip install uwsgi
$ pip install djangorestframework
```

## Set up DB ##

1.Create db `face_recognition`

```
$ mysql -u root -p

mysql> DROP DATABASE if exists face_recognition;
mysql> CREATE DATABASE face_recognition;
```

2.Create user `airport`

```
$ mysql -u root -p

mysql> CREATE USER 'admin'@'localhost' IDENTIFIED BY '#{THE_PASSWORD_FOR_AIPORT_ACCOUNT}';
```

3.Grant permission with `face_recognition` database

```
$ mysql -u root -p

mysql> GRANT ALL PRIVILEGES ON face_recognition.* TO 'airport'@'localhost';
```

4.Update MYSQL setting

Modify django face_reco_site/settings.py
Change DATABASES setting

5.Migrate the db schema

```
$ cd webapp/
$ python manage.py makemigrations
$ python manage.py migrate
```


## Start web server [Development]##

```
$ cd webapp/
$ python manage.py runserver 8080
```
## Start web server [Production]##

```
$ cd webapp/
$ uwsgi --ini uwsgi.ini
```

## List routes ##

```
$ cd webapp/
$ python manage.py show_urls

/									main.views.EnrollmentView	
/api/								rest_framework.routers.APIRootView		api-root
/api/\.<format>/					rest_framework.routers.APIRootView		api-root
/api/face_feature/					main.views.FaceFeatureViewSet			face_feature-list
/api/face_feature/<pk>/				main.views.FaceFeatureViewSet			face_feature-detail
/api/face_feature/<pk>\.<format>/	main.views.FaceFeatureViewSet			face_feature-detail
/api/face_feature\.<format>/		main.views.FaceFeatureViewSet			face_feature-list
/api/match_job/						main.views.MatchJobViewSet				match_job-list
/api/match_job/<pk>/				main.views.MatchJobViewSet				match_job-detail
/api/match_job/<pk>\.<format>/		main.views.MatchJobViewSet				match_job-detail
/api/match_job\.<format>/			main.views.MatchJobViewSet				match_job-list
/api/user/							main.views.UserViewSet					user-list
/api/user/<pk>/						main.views.UserViewSet					user-detail
/api/user/<pk>\.<format>/			main.views.UserViewSet					user-detail
/api/user\.<format>/				main.views.UserViewSet					user-list
/enrollment							main.views.EnrollmentView				main-enrollment_site
/live								main.views.LiveView						main-live_site
/recognition						main.views.RecognitionView				main-recognition_site
/media\/<path>						django.views.static.serve	
```

## Production Deployment ##
1. copy face_reco_nginx.conf to nginx configuration
2. sudo nginx -s reload
3. use uwsgi --ini uwsgi.ini
