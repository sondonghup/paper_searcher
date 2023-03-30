import uvicorn
import json
from argparse import ArgumentParser
from fastapi import FastAPI
from pydantic import BaseModel
from models.summarize import(
    load_model,
    predict
)

app = FastAPI(
    title = 'T5 summarize'
)

class SummarizeInput(BaseModel):
    text: str

class SummarizeOutput(BaseModel):
    summarizing: str

@app.post("/summarize", response_model=SummarizeOutput)
async def predict_chat(input: SummarizeInput):
    text = input.text
    result = predict(inputs= text, tokenizer=tokenizers, model=models)
    return SummarizeOutput(summarizing=result)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/v0.0.1-summarize.json")
    parse = parser.parse_args()
    config_path = parse.config
    config = json.load(open(config_path, encoding='utf-8'))

    tokenizers, models = load_model(config['summarize']['model_name'])
    print("[=!=]summarize model loaded[=!=]")
    uvicorn.run(app, host="0.0.0.0", port=config['deploy_port'])
