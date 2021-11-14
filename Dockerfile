FROM python:3.7.12-slim

RUN pip install -U pip setuptools

RUN pip install farm-haystack==0.10.0 --no-cache-dir
RUN pip install ray[default]==1.5.0

COPY . .

WORKDIR .

EXPOSE 8000

CMD ["uvicorn","server:app","--host","0.0.0.0","--port","8000"]