# Use lightweight Python base
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /wisdom

# Copy all files into the container
COPY . /wisdom

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Run the Wisdom Layer Streamlit app
CMD ["streamlit", "run", "llm_dashboard.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
