# Use Python 3.11
FROM python:3.11-slim

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app

# Install requirements
# Note: We use the backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r backend/requirements.txt

# Create necessary directories within the user's space
RUN mkdir -p $HOME/app/data

# Exposure port (Hugging Face Spaces default)
EXPOSE 7860

# Health Check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:7860/health')"

# Run the application using the app.py entry point
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
