import streamlit as st
from time import sleep
import requests

def per_generate(text, max_length=500, temperature=0.5, top_k=5, repetition_penalty=1.0, do_sample=False, use_cache=True):
    API_URL = "https://api-inference.huggingface.co/models/uripper/ChatbotTrainingBot"
    headers = {"Authorization": "Bearer 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"}
    
    if do_sample:
        use_cache = False
        
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": f"{text}",
        "parameters": {"max_new_tokens": max_length, "temperature": temperature, "top_k": top_k, "repitition_penalty": repetition_penalty, "do_sample": do_sample},
        "options": {"wait_for_model": True, "use_cache": use_cache},

    })
    return output
    
def gor_generate(text, max_length=500, temperature=0.5, top_k=5, repetition_penalty=1.0, do_sample=False, use_cache=True):
    API_URL = "https://api-inference.huggingface.co/models/uripper/Gordon"
    headers = {"Authorization": "Bearer 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"}
    
    if do_sample:
        use_cache = False

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    output = query({
        "inputs": f"{text}",
        "parameters": {"max_new_tokens": max_length, "temperature": temperature, "top_k": top_k, "repitition_penalty": repetition_penalty, "do_sample": do_sample},
        "options": {"wait_for_model": True, "use_cache": use_cache},

        })
    return output
    
def rev_generate(text, max_length=500, temperature=0.5, top_k=5, repetition_penalty=1.0, do_sample=False, use_cache=True):
    API_URL = "https://api-inference.huggingface.co/models/uripper/ReviewTrainingBot"
    headers = {"Authorization": "Bearer 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"}
    
    if do_sample:
        use_cache = False
        
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": f"{text}",
        "parameters": {"max_new_tokens": max_length, "temperature": temperature, "top_k": top_k, "repitition_penalty": repetition_penalty, "do_sample": do_sample},
        "options": {"wait_for_model": True, "use_cache": use_cache},
    })
    return output
    

if "persona_chat_history" not in st.session_state:
    st.session_state.persona_chat_history = []

if "gordon_chat_history" not in st.session_state:
    st.session_state.gordon_chat_history = []
    

def main_page():

    CHAT = False
    REVIEW = False
    


    st.title("Welcome!")
    st.write("This chatbot has a few interactive features, which can be accessed on the drop down menu on the left. \n\nThe first of these is the Review feature, the main feature of this application. You are able to enter the name of a movie and generate a review for it. This was created by finetuning a GPT-2 model on a dataset of movie reviews. The dataset was created via scraping around 120,000 letterboxd reviews. Currently, its main restrictions are that it hasn't found links between the movie title and the review itself, and struggles to determine positive and negative sentiment based on the score that is given. This will hopefully be improved with more reviews. However, it is excellent at generating formats of reviews, and will consistently give plausible reviews.")
    st.write("The next is the Gordon Chat feature. This is the main recommendation for chatting. This is a finetuned model of DialoGPT from Microsoft, which was trained on the movie lines dataset from Cornell. The corpus can be found at https://convokit.cornell.edu/documentation/movie.html.")
    st.write("The final feature is the Persona Chat feature. This is a finetuned model of distilgpt2 from Hugging Face, which was trained on the truecased Persona Chat dataset, found here https://huggingface.co/datasets/bavard/personachat_truecased. It is currently less capable of replying as consistently as Gordon, and will often reply with numerous exclamation points, after which it will proceed to change the subject. In order to make a less annoying and more coherent bot, you can select the feature 'Less Annoying' or if you want to see the full output, 'Normal'.")
        
def review():
    st.title("Review")
    
    temperature = st.slider("Temperature", 0.1, 1.0, 0.5, 0.01)
    top_k = st.slider("Top K", 1, 100, 5, 1)
    max_length = st.slider("Max Length", 1, 250, 100, 1)
    repetition_penalty = st.slider("Repetition Penalty (Affects future generations)", 0.0, 100.0, 1.0, 0.1)
    do_sample = st.checkbox("Do Sample (If unchecked, will use greedy decoding)")

    st.write("Please enter the name of the movie you would like to review.")
    in_movie = st.text_input("Movie")
    review_button = st.button("Generate Review")
    random_review = st.button("Random Review")
    if review_button: 
        in_movie = "Movie: " + in_movie + " Score:"
        output = rev_generate(in_movie, max_length=max_length, temperature=temperature, top_k=top_k, repetition_penalty=repetition_penalty, do_sample=do_sample)
        print(output)
        output = output[0]["generated_text"]
        out_movie =output.split("Score:")[0]
        out_movie = out_movie.replace("Movie: ", "")
        score = output.split("Review:")[0]
        score = score.split("Score:")[1]
        review = output.split("Review:")[1] 

        review = review.replace("…", ".")
        review = review.replace("...", ".")

        st.write("Movie:")
        st.write(out_movie)
        st.write("Score:")
        st.write(score)
        st.write("Review:")
        st.write(review)
    
    if random_review:
        output = rev_generate("Movie:", max_length=max_length, temperature=temperature, top_k=top_k, repetition_penalty=repetition_penalty, do_sample=do_sample)
        print(output)
        output = output[0]["generated_text"]
        out_movie =output.split("Score:")[0]
        out_movie = out_movie.replace("Movie: ", "")
        score = output.split("Review:")[0]
        score = score.split("Score:")[1]
        review = output.split("Review:")[1] 
        
        review = review.replace("…", ".")
        review = review.replace("...", ".")

        st.write("Movie:")
        st.write(out_movie)
        st.write("Score:")
        st.write(score)
        st.write("Review:")
        st.write(review)
        


def persona():   
    st.title("Persona Chat")
    st.write("Please enter your message below.")
    
    temperature = st.slider("Temperature", 0.1, 1.0, 0.5, 0.1)
    top_k = st.slider("Top K", 1, 100, 5, 1)
    max_length = st.slider("Max Length", 1, 250, 10, 1)
    repetition_penalty = st.slider("Repetition Penalty (Affects future generations)", 0.0, 100.0, 1.0, 0.1)
    do_sample = st.checkbox("Do Sample (If unchecked, will use greedy decoding)")
  

    user_chat = st.text_input("Chat with Persona!")
    stan_chat_button = st.button("Send")    

    if stan_chat_button:
        
        
        user_chat = "User: " + user_chat
        st.session_state.persona_chat_history.append(user_chat)
        st.write(user_chat)
        user_chat = user_chat + " Bot:"
        output = per_generate(user_chat, max_length=max_length, temperature=temperature, top_k=top_k, repetition_penalty=repetition_penalty, do_sample=do_sample)
        print(output)
        output = output[0]["generated_text"]
        output = output.split("Bot:")[1]
        output = "Persona: " + output


    
        
def gordon_chat():
    st.sidebar.title("Gordon Chat")
    st.title("Chat with Gordon")
    st.write("Please enter your message below.")
    
    temperature = st.slider("Temperature", 0.1, 1.0, 0.5, 0.1)
    top_k = st.slider("Top K", 1, 100, 5, 1)
    max_length = st.slider("Max Length", 1, 250, 10, 1)
    repetition_penalty = st.slider("Repetition Penalty (Affects future generations)", 0.0, 100.0, 1.0, 0.1)
    do_sample = st.checkbox("Do Sample (If unchecked, will use greedy decoding)")

    user_chat = st.text_input("Chat with Gordon!")
    gordon_chat_button = st.button("Send")    

    if gordon_chat_button:
        
        
        user_chat = "User: " + user_chat
        st.session_state.gordon_chat_history.append(user_chat)
        st.write(user_chat)
        user_chat = user_chat + " Bot:"
        output = gor_generate(user_chat, max_length=max_length, temperature=temperature, top_k=top_k, repetition_penalty=repetition_penalty)
        print(output)
        output = output[0]["generated_text"]        
        output = output.split("Bot:")[1]
        output = "Gordon: " + output
        st.write(output)


page_names_to_funcs = {
    "Main Page": main_page,
    "Review": review,
    "Gordon Chat": gordon_chat,
    "Persona Chat": persona,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

