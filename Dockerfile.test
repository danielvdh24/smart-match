# Use an official Python base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the entire application code into the working directory
COPY . /app/

# Install system dependencies (curl, bzip2, and ca-certificates)
RUN apt-get update && apt-get install -y \
    curl \
    bzip2 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda (a lightweight version of Anaconda)
RUN curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh \
    && bash miniconda.sh -b -p /opt/conda \
    && rm miniconda.sh \
    && /opt/conda/bin/conda init

# Add conda to PATH
ENV PATH="/opt/conda/bin:$PATH"

# Copy the environment.yml file into the container
COPY environment.yml /app/

# Create the Conda environment based on the environment.yml file
RUN conda env create -f environment.yml

# Ensure the environment is activated
RUN echo "conda activate resume_env" >> ~/.bashrc

# Expose the port the Django app will run on
EXPOSE 8000

# Run Django tests
CMD ["bash", "-c", "source ~/.bashrc && python manage.py test"]
