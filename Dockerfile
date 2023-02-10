FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04 AS compile-image
ENV PATH="/root/.cargo/bin:${PATH}"
WORKDIR /app

# Install required packages
RUN set -xe \
 && apt-get -y update \
 && apt-get install -y software-properties-common curl build-essential \
 && apt-get -y update \
 && add-apt-repository universe \
 && apt-get -y update \
 && apt-get -y install python3 python3-pip \
 && apt-get clean

# Install Rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

# Install python packages
COPY requirements.txt ./
RUN set -xe \
 && pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

CMD ["python3.10", "/app/app.py"]
