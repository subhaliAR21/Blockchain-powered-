# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY application/requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Set environment variable for Streamlit to run on all interfaces
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run the Streamlit app with explicit server address binding to 0.0.0.0 for Codespaces compatibility and port 8600
CMD ["streamlit", "run", "application/app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.enableCORS=false"]
