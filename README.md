# ruGPT-3 in Docker

Small API project based on Flesk for making requests to RuGPT-3 neural network.

## How to install

First need to build a composition:

```
docker-compose build
```

Run application:

```
docker-compose up -d
```

## How to use

Need to create POST request with JSON object.

```
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"prompt":"some text for network"}'
```
