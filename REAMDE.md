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
   4. Apply migrations
       ~~~
       $ python manage.py migrate
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