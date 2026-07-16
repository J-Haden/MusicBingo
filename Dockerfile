FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libreoffice fontconfig && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY fonts /usr/share/fonts/truetype/custom

RUN fc-cache -f -v

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

EXPOSE 5000

CMD ["python", "app.py"]