# Use an official, lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy ONLY the requirements file first. 
# This is a crucial DevOps practice called "Layer Caching". 
# It prevents Docker from re-installing all packages every time you change a line of Python code.
COPY configload.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r configload.txt

# Now copy the rest of your application code into the container
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the application
# We use --host=0.0.0.0 to make it accessible outside the container
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]