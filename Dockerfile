# Gunakan image Python resmi
FROM python:3.10-slim

# Set direktori kerja di dalam container
WORKDIR /app

# Salin semua file ke direktori kerja container
COPY . .

# Install dependencies dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port default Hugging Face Space
EXPOSE 7860

# Jalankan aplikasi Flask
CMD ["python", "app.py"]
