FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
# Run pip install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8501
CMD streamlit run main.py
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]