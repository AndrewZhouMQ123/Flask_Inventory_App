# first we want to get the appropriate baseimage for our python version
# python version 3.9.5, 3 types: slim-buster, alpine, slim bullseye
# look up documentation for more details
FROM python:3.9.5-slim-buster

# we want to define a working directory
WORKDIR /flask_inventory_app
# copy <the file we want to copy> <we give a name for the copied file>
COPY requirements.txt requirements.txt
# tell docker to run this command to install the requirements from the copied file
RUN pip3 install -r requirements.txt
# copy everything in the current directory, to the current directory in the server
COPY . .

# the flask app is where the main.py is located, here we create flask_app = create_app() 
ENV FLASK_APP=main.py
# since we create our db using sqlite3 in flask app
# we also need to tell docker to run these commands inside directory where flask app is
# use one line to reduce the layers in docker
RUN flask db init && flask db migrate && flask db upgrade

# run the following command to run the application
CMD ["python3", "main.py"]