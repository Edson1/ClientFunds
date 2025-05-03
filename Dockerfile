# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install. Install dependencies in PDN with --no-cache-dir
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Run the APP server, without debug level for PDN environment
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level","debug"]
    #LOCAL RUN> python -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug