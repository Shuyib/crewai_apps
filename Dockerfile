# Use an official Python runtime as a parent image
FROM python:3.10.12-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed debian packages and those specified in requirements.txt
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    git \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/* \ 
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Make port 8502 available to the world outside this container
EXPOSE 8504

# Add healthcheck
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:8504/ || exit 1


# Run app.py when the container launches
ENTRYPOINT [ "streamlit", "run" ]
CMD [ "app.py" ]
