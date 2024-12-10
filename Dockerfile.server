# Use the official Miniconda image as the base image
FROM continuumio/miniconda3

# Set the working directory inside the container
WORKDIR /app

# Copy the environment.yml file to the container
COPY environment.yml /app/

# Create the Conda environment inside the container
RUN conda env create -f environment.yml

# Activate the environment and install dependencies
SHELL ["conda", "run", "--no-capture-output", "-n", "resume_env", "/bin/bash", "-c"]

# Copy the rest of the application
COPY . /app/

# Expose the Django app port
EXPOSE 8000

# Set the environment variable for Django to use the correct Python environment
ENV PATH /opt/conda/envs/resume_env/bin:$PATH

# Run the Django development server
CMD ["conda", "run", "-n", "resume_env", "python", "manage.py", "runserver", "0.0.0.0:8000"]
