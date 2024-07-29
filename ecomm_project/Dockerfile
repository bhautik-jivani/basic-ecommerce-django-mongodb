FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /backend/
