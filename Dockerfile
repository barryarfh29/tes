FROM python:3.11-slim

# Install dependencies sistem untuk tgcrypto (opsional tapi bagus untuk kecepatan)
RUN apt-get update && apt-get install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file project
COPY . .

# Jalankan script (Ganti nama file jika berbeda)
CMD ["python", "-u", "pengambil.py"]
