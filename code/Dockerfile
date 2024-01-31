# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /client

# Copy the current directory contents into the container at /app
COPY . ./client

# Expose the port that the server will run on
EXPOSE 8000

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r client/requirements.txt

# Run client.py when the container launches
CMD ["python", "main.py"]
