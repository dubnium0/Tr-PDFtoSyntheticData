# Python 3.10 tabanlı bir imaj kullan
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y curl

# MODELI INDIR
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

COPY . .

RUN echo '#!/bin/bash\n\
uvicorn app:app --host 0.0.0.0 --port 8000 &\n\
# Backend hazır olana kadar bekle\n\
until $(curl --output /dev/null --silent --head --fail http://localhost:8000/docs); do\n\
    echo "Backend bekleniyor..."\n\
    sleep 2\n\
done\n\
streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0\n' > start.sh && chmod +x start.sh

EXPOSE 8000 8501

CMD ["/bin/bash", "./start.sh"]     