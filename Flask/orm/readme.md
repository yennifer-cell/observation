1. install psycopg2 <connect to our postgres db>
2. install python dotenv.<parse environemntal variable>
3. setup project folder structure
   -orm.py <custom orm>
   -db.py <db connections>
   -app.py <flask routes and controllers>
   -.env<environmental variable dont share with anyone>

4.setup the environemt and
download all packages using pipenv
  pipenv install psycopg2-binary python-dotenv
