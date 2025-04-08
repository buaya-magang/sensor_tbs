# Gunakan Python versi ringan
FROM python:3.10-slim

# Set direktori kerja
WORKDIR /app

# Salin semua file
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Buka port default HF
EXPOSE 7860

# Jalankan Flask
CMD ["python", "app.py"]
