

# create db on your beekeeper studio using postgresql
# setting up our project folder structure
pipenv shell

# install dependencies
pipenv install "uvicorn[standard]" prisma 
# initialize prisma
pipenv run prisma init
pipenv run prisma validate
pipenv run prisma db push
pipenv run prisma generate
pipenv run python app.py
--connect to your db

--next step
--we start with the routes we begin with ; user member routes 
we decide what a member can do; 1. signup<create an account>
                                2 login<authentication>

-- for data validation use pydantic
pipenv install pydantic 'pydantic[email]'

--Other routes
CRUD for product
  create read update delete
