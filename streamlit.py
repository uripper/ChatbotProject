import streamlit as st
from time import sleep
import requests

def per_generate(text, min_length=50, max_length=500, temperature=0.5, top_k=5, no_repeat_ngram_size=2):
    API_URL = "https://api-inference.huggingface.co/models/uripper/ChatbotTrainingBot"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": f"{text}",
        "parameters": {min_length: min_length, max_length: max_length, temperature: temperature, top_k: top_k, no_repeat_ngram_size: no_repeat_ngram_size},

    })
    return output
    
def gor_generate(text, min_length=50, max_length=500, temperature=0.5, top_k=5, no_repeat_ngram_size=2):
    API_URL = "https://api-inference.huggingface.co/models/uripper/Gordon"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    output = query({
        "inputs": f"{text}",
        "parameters": {min_length: min_length, max_length: max_length, temperature: temperature, top_k: top_k, no_repeat_ngram_size: no_repeat_ngram_size},

        })
    return output
    
def rev_generate(text, min_length=50, max_length=500, temperature=0.5, top_k=5, no_repeat_ngram_size=2):
    API_URL = "https://api-inference.huggingface.co/models/uripper/ReviewTrainingBot"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": f"{text}",
        "parameters": {min_length: min_length, max_length: max_length, temperature: temperature, top_k: top_k, no_repeat_ngram_size: no_repeat_ngram_size},
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
    max_length = st.slider("Max Length", 200, 1000, 500, 1)
    min_length = st.slider("Min Length", 50, 200, 50, 1)
    no_repeat_ngram_size = st.slider("No Repeat Ngram Size", 0, 10, 2, 1)   
    st.write("Please enter the name of the movie you would like to review.")
    in_movie = st.text_input("Movie")
    in_movie = "Movie: " + in_movie + " Score:"
    output = rev_generate(in_movie, min_length=min_length, max_length=max_length, temperature=temperature, top_k=top_k, no_repeat_ngram_size=no_repeat_ngram_size)
    output = output[0]["generated_text"]
    out_movie =output.split("Score:")[0]
    score = output.split("Review:")[0]
    review = output.split("Review:")[1] 
    
    
    st.write(output)
    st.write("Movie:")
    st.write(out_movie)
    st.write("Score:")
    st.write(score)
    st.write("Review:")
    st.write(review)
    # if movie != "":
    #     review, movie, score, review = reviewing.generating_review(movie,
    #                                                                temperature=temperature,
    #                                                                top_k=top_k,
    #                                                                max_length=max_length,
    #                                                                min_length=min_length,
    #                                                                no_repeat_ngram_size=no_repeat_ngram_size)
                                                                       
    #     st.write(movie)
    #     st.write(score)
    #     st.write(review)

def persona():   
    st.title("Persona Chat")
    annoying = st.selectbox("Normal or Less Annoying?", ["Normal", "Less Annoying"])
    st.write("Please enter your message below.")
    temperature = st.slider("Temperature", 0.1, 1.0, 0.5, 0.1)
    top_k = st.slider("Top K", 1, 100, 5, 1)
    max_length = st.slider("Max Length", 10, 1000, 15, 1)
    min_length = st.slider("Min Length", 1, 200, 1, 1)
    no_repeat_ngram_size = st.slider("No Repeat Ngram Size", 0, 10, 2, 1)    

    user_chat = st.text_input("Chat with Persona!")
    stan_chat_button = st.button("Send")    

    if stan_chat_button:
        
        
        user_chat = "User: " + user_chat
        st.session_state.persona_chat_history.append(user_chat)
        st.write(user_chat)
        user_chat = user_chat + " Bot:"
        output = per_generate(user_chat, min_length=min_length, max_length=max_length, temperature=temperature, top_k=top_k, no_repeat_ngram_size=no_repeat_ngram_size)
        output = output[0]["generated_text"]
        output = output.split("Bot:")[1]
        st.write(output)
        # bot_response = "Bot: " + bot_response
        # if annoying == "Less Annoying":
        #     if "!!" in bot_response:
        #         bot_response = bot_response.split("!!")[0]
        # st.session_state.persona_chat_history.append(bot_response)
        # st.write(bot_response)
        
        sleep(1)
        st.write("_" * 50)
        st.write("Chat History:")
        for i in st.session_state.persona_chat_history:
            st.write(i)   

    
        
def gordon_chat():
    st.sidebar.title("Gordon Chat")
    st.title("Chat with Gordon")
    st.write("Please enter your message below.")
    
    temperature = st.slider("Temperature", 0.1, 1.0, 0.5, 0.01)
    top_k = st.slider("Top K", 1, 100, 5, 1)
    max_length = st.slider("Max Length", 10, 1000, 15, 1)
    min_length = st.slider("Min Length", 1, 200, 1, 1)
    no_repeat_ngram_size = st.slider("No Repeat Ngram Size", 0, 10, 2, 1)     
    user_chat = st.text_input("Chat with Gordon!")
    gordon_chat_button = st.button("Send")    

    if gordon_chat_button:
        
        
        user_chat = "User: " + user_chat
        st.session_state.gordon_chat_history.append(user_chat)
        st.write(user_chat)
        user_chat = user_chat + " Bot:"
        output = gor_generate(user_chat, min_length=min_length, max_length=max_length, temperature=temperature, top_k=top_k, no_repeat_ngram_size=no_repeat_ngram_size)
        print(output)
        output = output[0]["generated_text"]        
        output = output.split("Bot:")[1]
        st.write(output)
        # st.session_state.gordon_chat_history.append(bot_response)
        # st.write(bot_response)
        
        # sleep(1)
        # st.write("_" * 50)
        # st.write("Chat History")
        # for i in st.session_state.gordon_chat_history:
        #     st.write(i)   

page_names_to_funcs = {
    "Main Page": main_page,
    "Review": review,
    "Gordon Chat": gordon_chat,
    "Persona Chat": persona,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

