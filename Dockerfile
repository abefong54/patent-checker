FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# STREAMLIT PORT
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501"]
