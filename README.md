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
       2. $ python manage.py migrate adv_board
       3. $ python manage.py migrate 
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
    
###NOTES:
1. Filtering is performed by get request on announcements list, via category name:
    ~~~
    http://127.0.0.1:8000/api/announcements/?category=Appliances
    ~~~
    the above get request will output all announcements that belongs
    to Appliances and their subcategories