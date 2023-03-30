from transformers import (
    BartForConditionalGeneration,
    PreTrainedTokenizerFast
)

def load_model(model_name):
    tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name).eval().to(device='mps')
    return tokenizer, model

def predict(inputs, tokenizer, model):
    encoded_inputs = tokenizer(inputs, return_tensors="pt").to(device='mps')
    outputs = model.generate(encoded_inputs['input_ids'])
    
    generated = tokenizer.decode(outputs[0], skip_special_tokens = True)
    return generated
