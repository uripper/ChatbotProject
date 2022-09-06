print("Warming up review bot...")


from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import torch.nn.functional as F

tokenizer = GPT2Tokenizer.from_pretrained('uripper/ReviewTrainingBot')
model = GPT2LMHeadModel.from_pretrained('uripper/ReviewTrainingBot')


def generating_review(text, max_length=300):
    prompt = f"<|startoftext|> {text}"
    new_max_length = max_length + len(prompt)
    generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
    outputs = model.generate(
        generated, 
        max_length=new_max_length, 
        pad_token_id=tokenizer.pad_token_id, 
        bos_token_id=tokenizer.bos_token_id, 
        eos_token_id=tokenizer.eos_token_id,
        min_length=len(prompt)+1,
        do_sample=True, 
        top_k=50, 
        top_p=0.95, 
        temperature=.6, 
        no_repeat_ngram_size=3,
        num_beams=1,
        )
    output = tokenizer.decode(outputs[0])
    new_output = output.replace("<|endoftext|>","").replace("<|pad|>","").replace("<|startoftext|>", "")
    score_list = new_output.split("Score: ")
    movie_raw = score_list[0]
    movie = movie_raw.replace("Movie: ","")
    score_raw = score_list[-1]
    review_raw = score_raw.split("Review: ")
    score = review_raw[0].replace("Review: ", "")
    review = review_raw[1]
    if review.startswith(" "):
        review = review[1:]
    if review[-2] == "…":
        review_list = review.split(". ")
        review_list.remove(review_list[-1])
        review = ". ".join(review_list)
    review.replace("\n", "")
    if review.endswith(" ") and not review.endswith(". "):
        review = review[:-1]
        review = review + "."
    if review.endswith(".") == False:
        review = review + "."
    output_final = f"""
Movie: {movie}
Score: {score}
Review: {review}
"""
    return output_final, movie, score, review

#This will run a test immediately, which will load the model as the program begins 
#this allows for a faster response time when the user inputs text
generated, x, y, z = generating_review("Movie:", max_length=10)
print("Test response (should be shorter than usual): ")
print(generated)
print("Review bot is ready to go!")
print("-"*50)