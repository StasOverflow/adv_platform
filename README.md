##Advertisement platfrom

Dev notes: 
    
- To start your development on a new machine:
   1. Install requirements
       ~~~
       $ pip install -r requirements.txt
       ~~~
   2. Import environment variables into your terminal:
      ~~~
      $ . .env
      ~~~
   3. Create database (project is using PostgreSQL)
       ~~~
       $ sudo su - postgres
       $ psql
       ~~~
       database name, user name and pass are specified in
       .env file
       ~~~
       $ CREATE DATABASE adv_platform; 
       $ CREATE USER olxer WITH PASSWORD 'olxer';
       $ GRANT ALL PRIVILEGES ON DATABASE adv_platform TO olxer;
       ~~~
   4. Apply migrations (ordering is important!)
       ~~~
       1. $ python manage.py migrate users
       2. $ python manage.py migrate allauth
       3. $ python manage.py migrate adv_board
       5. $ python manage.py migrate 
       ~~~
       to unapply migrations, run:
       ~~~
       $ python manage.py migrate adv_board zero
       ~~~
       
   5. Apply fixtures
       ~~~
       $ python manage.py loaddata superuser.json
       $ python manage.py loaddata category.json
       ~~~
- Run

   ~~~     
    $ python manage.py runserver
   ~~~
- Admin panel can be accessed with 

   ~~~
    login: 'admin' 
     pass: 'super_admin'
   ~~~
- Site API can be accessed via:
    ~~~
    http://127.0.0.1:8000/api/docs
    ~~~
- To run tests:
    1. Grant previlegies to create database to our 
    database user (olxer, according to .env file)
        ~~~
        $ sudo su - postgres
        $ psql
        $ ALTER USER olxer CREATEDB;
        ~~~
    2. Run tests
    
#### To run celery task (set announcement as inactive every 30 days)

1. Make sure you have redis on your machine
2. run celery -A adv_board worker --loglevel=info -B


#### More notes:

Credentials for site users are:

1. log: Customer
  pass: olxerolxer123
   
2. log: JohnnyCash
  pass: mancomesAround1948
