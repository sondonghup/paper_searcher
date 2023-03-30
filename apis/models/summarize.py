import os
from transformers import (
    AutoTokenizer,
    T5ForConditionalGeneration
)

def load_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token = True,
                                                        bos_token='[BOS]',
                                                        eos_token='[EOS]', 
                                                        unk_token='[UNK]', 
                                                        pad_token='[PAD]', 
                                                        mask_token='[MASK]'
                                                        )
    model = T5ForConditionalGeneration.from_pretrained(model_name, use_auth_token = True).eval()
    return tokenizer, model

def predict(inputs, tokenizer, model):
    encoded_inputs = tokenizer.encode(inputs, return_tensors="pt")
    outputs = model.generate(encoded_inputs,
                            pad_token_id = tokenizer.pad_token_id,
                            max_length=160,
                            num_beams=1,
                            length_penalty=1.2,
                            early_stopping=True,
                            use_cache=True
                            )
    
    generated = tokenizer.decode(outputs[0], skip_special_tokens = True)
    return generated
