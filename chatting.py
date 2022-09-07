print("Warming up Persona...")

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import torch.nn.functional as F

tokenizer = GPT2Tokenizer.from_pretrained('uripper/ChatbotTrainingBot')

model = GPT2LMHeadModel.from_pretrained('uripper/ChatbotTrainingBot')


def generating_reply(text, max_length=300, top_k=5, temperature=.7, min_length=1, no_repeat_ngram_size=2):
    
    prompt = f"<|startoftext|> {text}"
    generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
    outputs = model.generate(
        generated, 
        max_length=max_length,
        pad_token_id=tokenizer.pad_token_id, 
        bos_token_id=tokenizer.bos_token_id, 
        eos_token_id=tokenizer.eos_token_id,
        min_length=min_length,
        do_sample=True,  
        top_k=top_k, 
        temperature=temperature,
        no_repeat_ngram_size= no_repeat_ngram_size
        )
    output = tokenizer.decode(outputs[0])
    new_output = output.replace("<|endoftext|>","").replace("<|pad|>","")
    output_list = new_output.split("Bot: ")
    output_raw_response = output_list[-1]
    output_semi_final = output_raw_response.replace("Bot: ","")
    if "User:" in output_semi_final:
        output_new_list = output_semi_final.split("User: ")
        output_final = output_new_list[0]
    else:
        output_final = output_semi_final
    return output_final

#This will run a test immediately, which will load the model as the program begins 
#this allows for a faster response time when the user inputs text
generated = generating_reply("Hello", max_length=10)
print("Test response (should be shorter than usual): ")
print(generated)
print("Chatbot is ready to go!")
print("-"*50)