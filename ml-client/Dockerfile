# in Docker, it is common to base a new image on a previously-created image
# Use an official Python runtime image as a parent image to base this image on
FROM python:3.7-slim

# Set the working directory within the image to the correct working directory /ml-client
WORKDIR /ml-client

# the ADD command is how you add files from your local machine into a Docker image
# Copy the current directory contents into the container at /ml-client
ADD . /ml-client

# Install and update essential meta-packages, which is necessary to compiling software
RUN apt-get update && apt-get install build-essential -y

# Install python package manager pip
RUN python -m pip install --upgrade pip

# Install cmake, pytest for compilation and testing
RUN pip3 install cmake 
RUN pip3 install pytest
# Install all the required packages in requirements.txt
RUN pip3 install -r requirements.txt

# By default Docker containers are closed off to the external world
# Copy all everything in the current directory into WORKDIR
# from the host system into the image
COPY . .

# Make port 7001 available to the world outside this container
EXPOSE 3000

# Run app.py when the container launches
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=3000"]