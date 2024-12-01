# Use an official Python base image
FROM python:3.8-slim

# Install Miniconda (a lightweight version of Anaconda)
RUN apt-get update && apt-get install -y curl bzip2 ca-certificates \
    && curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh \
    && bash miniconda.sh -b -p /opt/conda \
    && rm miniconda.sh \
    && /opt/conda/bin/conda clean -tipsy \
    && ln -s /opt/conda/bin/conda /usr/local/bin/conda

# Set the working directory inside the container
WORKDIR /app

# Copy the environment.yml and the rest of your application code into the container
COPY environment.yml /app/
COPY . /app/

# Create the Conda environment from the environment.yml file
RUN conda env create -f environment.yml

# Activate the Conda environment and make it the default in the container
SHELL ["/bin/bash", "-c"]
RUN echo "conda activate myenv" >> ~/.bashrc

# Expose the port the Django app will run on
EXPOSE 8000

# Command to run Django's development server
CMD ["bash", "-c", "source ~/.bashrc && python manage.py runserver"]
