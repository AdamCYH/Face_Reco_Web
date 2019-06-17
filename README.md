This is a face matcher website.
It does not include enrollment.


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
```

## Set up DB ##

1.Create db `registry`

```
$ mysql -u root -p

mysql> DROP DATABASE if exists registry;
mysql> CREATE DATABASE registry;
```

2.Create user `airport`

```
$ mysql -u root -p

mysql> CREATE USER 'airport'@'localhost' IDENTIFIED BY '#{THE_PASSWORD_FOR_AIPORT_ACCOUNT}';
```

3.Grant permission with `registry` database

```
$ mysql -u root -p

mysql> GRANT ALL PRIVILEGES ON registry.* TO 'airport'@'localhost';
```

4.Update `my.cnf` file

```
$ sudo vim /etc/mysql/my.cnf

[client]
database = registry
user = airport
password = #{THE_PASSWORD_FOR_AIPORT_ACCOUNT}
default-character-set = utf8mb4

$ sudo /etc/init.d/mysql stop
$ sudo /etc/init.d/mysql start
```

5.Migrate the db schema

```
$ cd webapp/
$ python manage.py makemigrations
$ python manage.py migrate
```

6.Create the `admin` account for dashboard

```
USE registry;
INSERT INTO admin (name, role, user_name, password, email, phone) VALUES ("admin", "admin", "admin", "#{THE_PASSWORD_FOR_ADMIN_ACCOUNT}", "admin@admin.com", 0800);
```


## Start web server ##

```
$ cd webapp/
$ python manage.py runserver 8080
```

## List routes ##

```
$ cd webapp/
$ python manage.py show_urls

/       						registry.views.home     				registry-home
/dashboard/     				dashboard.views.dashboard_site  		dashboard
/dashboard/admin        		dashboard.views.manage_admin    		dashboard-admin
/dashboard/admin_management     dashboard.views.admin_management_site   dashboard-admin_management
/dashboard/check_feature_status dashboard.views.feature_status  		dashboard-check_feature_status
/dashboard/dashboard_summary    dashboard.views.dashboard_summary       dashboard-dashboard_summary
/dashboard/detection    		dashboard.views.detection       		dashboard-detection
/dashboard/live 				dashboard.views.live_site       		dashboard-live
/dashboard/load_features        dashboard.views.load_face_feature       dashboard-load_features
/dashboard/load_test_data       dashboard.views.load_test_data  		dashboard-load_test_data
/dashboard/login        		dashboard.views.login   				dashboard-login
/dashboard/logout       		dashboard.views.logout  				dashboard-logout
/dashboard/member_management    dashboard.views.member_management_site  dashboard-member_management
/dashboard/registration_check   dashboard.views.registration_check      dashboard-registration_check
/dashboard/security_check       dashboard.views.security_check_site     dashboard-security-check
/dashboard/update_face_feature  dashboard.views.update_feature  		dashboard-update_feature
/dashboard/update_leave_time    dashboard.views.update_leave_time       dashboard-update_leave_time
/dashboard/validate_username    dashboard.views.validate_username       dashboard-validate_username
/dashboard/visitor_api  		dashboard.views.visitor_api     		dashboard-visitor_api
/home_upload    				registry.views.home_upload      		registry-home_upload
/media\/<path>  				django.views.static.serve
/registration   				registry.views.registration     		registry-registration
/rtsp   						registry.views.home_rtsp        		registry-rtsp
```

## Production Deployment ##
1. copy airport.conf to nginx configuration
2. sudo nginx -s reload
3. use start_service.sh to start service

