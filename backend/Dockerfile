FROM python:3.10-slim

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Set Python path so it can find 'agents' package when run from inside /app/backend
ENV PYTHONPATH=/app/backend

# Groq API key — pass at runtime: docker run -e GROQ_API_KEY=your_key ...
ENV GROQ_API_KEY=""

WORKDIR /app/backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
