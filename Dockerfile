FROM python:3.10-slim
LABEL authors="mhasan502"

WORKDIR /code
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY app/ app/

CMD ["/bin/bash"]
