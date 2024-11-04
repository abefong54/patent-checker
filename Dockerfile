# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .


# specify compatibility with the --use-pep517 flag for python 3.9
# Install the dependencies
RUN pip install --no-cache-dir --use-pep517 -r requirements.txt

# Copy the entire application into the container
COPY . .

# Expose the port Streamlit uses
EXPOSE 8501

# Command to run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
