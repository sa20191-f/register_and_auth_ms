# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6

RUN apt-get update && apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev
# RUN apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev

# The enviroment variable ensures that the python output is set straight to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /users_ms

# Set the working directory to /music_service
WORKDIR /users_ms

# Copy the current directory contents into the container at /music_service
ADD . /users_ms/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 3001
