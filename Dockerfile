# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get update && apt-get install -y graphviz
# Copy the rest of the app code into the container
COPY . .

# Expose the port that Streamlit listens on
EXPOSE 8501

# Run the app when the container launches
CMD ["streamlit", "run", "Home.py"]