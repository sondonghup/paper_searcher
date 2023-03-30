import uvicorn
import json
from argparse import ArgumentParser
from fastapi import FastAPI
from pydantic import BaseModel
from models.translate import(
    load_model,
    predict
)

app = FastAPI(
    title = 'translate'
)

class TranslateInput(BaseModel):
    text: str

class TranslateOutput(BaseModel):
    Translating: str

@app.post("/translate", response_model=TranslateOutput)
async def predict_translate(input: TranslateInput):
    text = input.text
    result = predict(inputs= text, tokenizer=tokenizers, model=models)
    print(result)
    return TranslateOutput(Translating=result)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/v0.0.1-translate.json")
    parse = parser.parse_args()
    config_path = parse.config
    config = json.load(open(config_path, encoding='utf-8'))

    tokenizers, models = load_model(config['translate']['model_name'])
    print("[=!=]translate model loaded[=!=]")
    uvicorn.run(app, host="0.0.0.0", port=config['deploy_port'])
