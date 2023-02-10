import gc
import json
import torch
import numpy as np
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from flask import Flask, request, render_template
from werkzeug.exceptions import HTTPException

np.random.seed(42)
torch.manual_seed(42)
torch.__version__

app = Flask(__name__)

path = "sberbank-ai/rugpt3large_based_on_gpt2"
tok = GPT2Tokenizer.from_pretrained(path)
model = GPT2LMHeadModel.from_pretrained(path)

@app.errorhandler(HTTPException)
def handle_exception(e):
    torch.cuda.empty_cache()
    gc.collect()
    return json.dumps({"message": e.description}), e.code

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    # Parse request
    json_str = request.get_data()
    data = json.loads(json_str)

    # Sentence for work
    question = data['question']

    #
    # Settings
    #

    do_sample = True

    # Max length of output string
    max_length = 100
    if "max_length" in data:
        max_length = data['max_length']

    # Use default cuda device if available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    if "device" in data:
        device = data['device']

    # Use selected device
    model.to(torch.device(device))

    repetition_penalty = 5.0
    if "repetition_penalty" in data:
        repetition_penalty = data['repetition_penalty']

    top_k = 5
    if "top_k" in data:
        top_k = data['top_k']

    top_p = 0.95
    if "top_p" in data:
        top_p = data['top_p']

    temperature = 1
    if "temperature" in data:
        temperature = data['temperature']

    num_beams = 10
    if "num_beams" in data:
        num_beams = data['num_beams']

    no_repeat_ngram_size = 3
    if "no_repeat_ngram_size" in data:
        no_repeat_ngram_size = data['no_repeat_ngram_size']

    #
    # Init model
    #

    input_ids = tok.encode(question, return_tensors="pt").to(device)
    out = model.generate(
        input_ids,
        max_length=max_length,
        repetition_penalty=repetition_penalty,
        do_sample=do_sample,
        top_k=top_k,
        top_p=top_p,
        temperature=temperature,
        num_beams=num_beams,
        no_repeat_ngram_size=no_repeat_ngram_size
    )
    generated = list(map(tok.decode, out))
    output = {
        "predicted": generated[0],
        "question": question,
        "device": device,
        "do_sample": do_sample,
        "max_length": max_length,
        "repetition_penalty": repetition_penalty,
        "top_k": top_k,
        "top_p": top_p,
        "temperature": temperature,
        "num_beams": num_beams,
        "no_repeat_ngram_size": no_repeat_ngram_size
    }
    return json.dumps(output)


app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
