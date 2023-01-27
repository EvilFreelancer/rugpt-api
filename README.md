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
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"question":"some text for network"}'
```

## Supported parameters

| Name                 | Type   | Default |
|----------------------|--------|---------|
| question             | string |         |
| max_length           | int    | 100     |
| repetition_penalty   | float  | 5.0     |
| top_k                | int    | 5       |
| top_p                | float  | 0.95    |
| temperature          | int    | 1       |
| num_beams            | int    | 10      |
| no_repeat_ngram_size | int    | 3       |
