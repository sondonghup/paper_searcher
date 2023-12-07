from transformers import (
    M2M100ForConditionalGeneration,
    M2M100Tokenizer,
    MarianMTModel,
    MarianTokenizer
)

def load_model(model_name):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name).eval().to(device='cpu')
    return tokenizer, model

def predict(inputs, tokenizer, model):
    encoded_inputs = tokenizer(inputs, return_tensors="pt", padding = True, truncation = True).to(device='cpu')
    outputs = model.generate(**encoded_inputs)
    
    generated = tokenizer.decode(outputs[0], skip_special_tokens = True)
    return generated
