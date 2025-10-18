# ใช้ Python 3.11 slim image
FROM python:3.11-slim

# ตั้งค่า working directory
WORKDIR /app

# Install system dependencies สำหรับ reportlab
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

# สร้างฐานข้อมูลใหม่เมื่อรัน container
# Database จะถูกสร้างใหม่ทุกครั้งที่ start container
ENV PYTHONUNBUFFERED=1

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

