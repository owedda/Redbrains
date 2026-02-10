# 1. Use a lightweight Python base image
FROM python:3.9-slim

# 2. Set environment variables to keep Python clean
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy the requirements file first (for better caching)
COPY requirements.txt .

# 5. Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your code
COPY . .

# 7. Default command (this is overridden by docker-compose, but good to have)
CMD ["python", "-m", "src.sentinel"]