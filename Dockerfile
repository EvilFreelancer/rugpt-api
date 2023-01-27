FROM python:3.10-slim AS compile-image
ENV PATH="/root/.cargo/bin:${PATH}"
RUN apt-get update
RUN apt-get install -y --no-install-recommends curl build-essential
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
WORKDIR /app
COPY requirements.txt ./
RUN set -xe \
 && pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt


FROM python:3.10-slim
EXPOSE 5000
COPY --from=compile-image /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . .
CMD ["python", "/app/app.py"]
