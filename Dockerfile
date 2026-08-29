FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies with --break-system-packages
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copy app files
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose port (Cloud Run default)
EXPOSE 8501

# Run Streamlit using python -m
CMD ["python", "-m", "streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
