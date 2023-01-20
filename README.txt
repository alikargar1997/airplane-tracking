1- Run Postgresql,Redis-server,Rabbitmq-server on your system.
2- create a database and user in postgresql using the following:

sudo su - postgres
psql
CREATE USER myprojectuser WITH PASSWORD 'password';
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
\q
exit

3- Open airplane_monitoring/airplane_monitoring/settings.py and set your username and password in the DATABASES part. 
4- "cd" to project folder 
5- Run  "pip install -r requirements.txt"
6- Run "python manage.py makemigrations"
7- Run "python manage.py migtate"
8- Create a superuser by running "python manage.py createsuperuser"
9- Run "python manage.py runserver"
10- open 3 new terminals and cd into project folder
11- Run "celery -A airplane_monitoring worker --loglevel=INFO"
12- Run "celery -A airplane_monitoring beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler"
13- Run "python -m smtpd -n -c DebuggingServer localhost:1025" to monitor emails,i set the email settings to terminal smtp,
if you want to sending emails you have to set your smtp settings.

14- Now lets test the app:
- open "http://localhost:8000/admin" in the browser.
- enter your username/email and password.
- click on tracking->Flights to create a flight and click on "ADD FLIGHT"
- you should enter the flight informations refer to:
    Schedule delay: fill in minutes.crawling schedule delay.
    Informations file: it is the file to get data from it,no need to fill,the default is "crawler_result.json". 
    Flight number: must be unique.

** after adding the Flight ,crawler scheduler starts. you can see more informations in PERIODIC TASKS -> Periodic tasks

- logout the admin page (** YOU CAN CONTINUE WITHOUT LOGOUT,NO NEED TO SIGN IN OR SIGN UP.)
- open "http://localhost:8000/accounts/signup/" in your browser.
- Sign up a new user
- Login
- click on "create" to create a new flight tracking scheduler.
- choose your flight and set the schedule delay time in minutes
- now you can see the email results in your terminals refer to level 13.






-----------------Please contact me if you encountered any problems while using or installing the app------------------



