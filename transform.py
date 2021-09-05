from transformers import T5Tokenizer, GPT2LMHeadModel

tokenizer = T5Tokenizer.from_pretrained("./model/pretrained_model")
model = GPT2LMHeadModel.from_pretrained("./model/finetuned_model")

def generate(text):
    input = tokenizer.encode(text, return_tensors="pt")
    output = model.generate(input, do_sample=True, max_length=100, pad_token_id=tokenizer.eos_token_id)
    decoded = tokenizer.batch_decode(output, skip_special_tokens=True)
    return decoded[0]

if __name__ == "__main__":
    pass
