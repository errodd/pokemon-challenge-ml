FROM python:3.12-slim

WORKDIR /app

# Copy only what the app needs
COPY requirements-app.txt .
RUN pip install --no-cache-dir -r requirements-app.txt

COPY artifacts/ artifacts/
COPY data/pokemon.csv data/pokemon.csv
COPY src/ src/
COPY app.py .

EXPOSE 7860

CMD ["python", "app.py"]
