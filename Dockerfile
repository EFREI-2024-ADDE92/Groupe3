# Use an official Python runtime as a base image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /

# Copy the current directory contents into the container at /app
COPY . /

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=get_model.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]

#az login
#docker tag model_groupe3 efreibigdata.azurecr.io/model_groupe3:latest
#docker push efreibigdata.azurecr.io/model_groupe3:latest
#az acr repository list --name efreibigdata.azurecr.io --output table