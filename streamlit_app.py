import streamlit_app as st
import requests

BAD_WORD = False
my_api = st.secrets["my_api"]
bad_words = st.secrets["bad_words"]

def per_generate(text, max_length=500, temperature=0.5, top_k=5, do_sample=False, use_cache=True):
    API_URL = "https://api-inference.huggingface.co/models/uripper/ChatbotTrainingBot"
    headers = {"Authorization": f"Bearer {my_api}"}
    
    if do_sample:
        use_cache = False
        
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": f"{text}",
        "parameters": {"max_new_tokens": max_length, "temperature": temperature, "top_k": top_k, "do_sample": do_sample},
        "options": {"wait_for_model": True, "use_cache": use_cache},

        })
    return output
    
def gor_generate(text, max_length=500, temperature=0.5, top_k=5, do_sample=False, use_cache=True):
    API_URL = "https://api-inference.huggingface.co/models/uripper/Gordon"
    headers = {"Authorization": f"Bearer {my_api}"}
    
    if do_sample:
        use_cache = False

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    output = query({
        "inputs": f"{text}",
        "parameters": {"max_new_tokens": max_length, "temperature": temperature, "top_k": top_k, "do_sample": do_sample},
        "options": {"wait_for_model": True, "use_cache": use_cache},

        })
    return output
    
def rev_generate(text, max_length=500, temperature=0.5, top_k=5, do_sample=False, use_cache=True):
    API_URL = "https://api-inference.huggingface.co/models/uripper/ReviewTrainingBot"
    headers = {"Authorization": f"Bearer {my_api}"}
    
    if do_sample:
        use_cache = False
        
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": f"{text}",
        "parameters": {"max_new_tokens": max_length, "temperature": temperature, "top_k": top_k, "do_sample": do_sample},
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
    


    st.title("Welcome to this multi function chatbot!")
    st.write("This chatbot has a few interactive features, which can be accessed on the drop down menu on the left. \n\nThe first of these is the Review feature, the main feature of this application. You are able to enter the name of a movie and generate a review for it. This was created by finetuning a GPT-2 model on a dataset of movie reviews. The dataset was created via scraping around 120,000 letterboxd reviews.")
    st.write("The next is the Gordon Chat feature. This is the main recommendation for chatting. This is a finetuned model of DialoGPT from Microsoft, which was trained on the movie lines dataset from Cornell. The corpus can be found at https://convokit.cornell.edu/documentation/movie.html. It is recommended to use greedy search for this model in order to create the most likely responses to text. Its responses are fairly normal, with some abilities to act a specific role in response to a remark. For limitations, read the limitations section below.")
    st.write("The final feature is the Persona Chat feature. This is a finetuned model of distilgpt2 from Hugging Face, which was trained on the truecased Persona Chat dataset, found here https://huggingface.co/datasets/bavard/personachat_truecased. It is recommended to use greedy search for this model as well.")
    st.title("Limitations and biases")
    st.write("The main limitations of the review feature are that it is unable to find links between the movie title and the review itself, and struggles to determine positive and negative sentiment based on the score that is given. It however gives consistently plausible reviews, if not very plausible. It is unable to determine fact, and cannot give truthful reviews or reliably determine actors/directors for any given movie. Its main, and only, use case is for entertainment.")
    st.write("The review bot also has social biases. Due to its underlying model, it has many of the same biases as GPT-2. These biases can be found here: https://huggingface.co/gpt2. In addition to these biases, it also struggles with some of the unique examples of this training dataset. For a concrete example of this, it is fairly common for a review of a movie with gay or lesbian characters to be described as being 'very gay' on letterboxd.com. This is almost always used as a positive thing, but the bot itself is incapable of determining that this is a positive sentiment, and will describe random films this way in a manner that seems more like a slur. This language can likely be extended to other ways that have not been discovered yet, and the model should be handled with care.") 
    st.write("Gordon chat's main limitations are that it has difficulty understanding context and reasoning for how it should choose responses. The same can be seen in greedy searches in the model it is trained after, DialoGPT. This is a limitation of chatbots, as a whole, and is not unique to this model. Due to its usage of movie lines as a dataset, prioritization of dialog that may be unnatural or overly dramatic may be expected in some cases, though it does not seem to be very common in practice.")    
    st.write("Gordon chat also has social biases. Due to its underlying model, it has many of the same biases as DialoGPT. These biases can be found here: https://www.microsoft.com/en-us/research/project/large-scale-pretraining-for-response-generation/. In addition to these biases, it may have additional biases due to its training dataset. As films often use slurs in a variety of ways for a variety of purposes, these slurs can make their way into the results. In order to solve this, there will be a list of 'bad words' that will prevent output. ")
    st.write("Persona chat's main limitations are much of the same as Gordon chat. The responses have been subjectively rated as weaker than those of Gordon chat, but this may be due to personal preference, and your experience may vary.")
    st.write("Persona chat has many of the same social biases as distilgpt2, which can be found here: https://huggingface.co/distilgpt2. In addition to these biases, it may have additional biases due to its training dataset, although they have not been discovered yet during my testing. As a special precaution, its responses are also passed through a bad word filter, which will prevent output if it contains any of the words in the list.")

def review():
    BAD_WORD = False
    st.title("Review")
    
    temperature = st.slider("Temperature", 0.1, 1.0, 0.8, 0.01)
    top_k = st.slider("Top K", 1, 100, 15, 1)
    max_length = st.slider("Max Length", 1, 250, 100, 1)
    do_sample = st.checkbox("Do Sample (If unchecked, will use greedy decoding, not recommended for review due to repetition)", True)

    st.write("Please enter the name of the movie you would like to review. First generation may take up to a minute or more, as the model is loading. Latter generations should load faster.")
    in_movie = st.text_input("Movie")
    review_button = st.button("Generate Review")
    random_review = st.button("Random Review")
    st.write("Please only press Generate Review or Random Review once, it will take a short amount of time to load during the first generation.")
    if review_button: 
        in_movie = "Movie: " + in_movie + " Score:"
        output = rev_generate(in_movie, max_length=max_length, temperature=temperature, top_k=top_k, do_sample=do_sample)
                
        check_output = output[0]["generated_text"]
        check_output = check_output.split(" ")
        for i in check_output:
            for j in bad_words:
                if i.lower() is j:
                    BAD_WORD =True
                    
                
        print(output)
        output = output[0]["generated_text"]

        if BAD_WORD == True:

            st.write("The bot generated a slur, please try again.")
            BAD_WORD = False
        else:
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
        output = rev_generate("Movie:", max_length=max_length, temperature=temperature, top_k=top_k, do_sample=do_sample)     
        check_output = output[0]["generated_text"]
        check_output = check_output.split(" ")
        for i in check_output:
            for j in bad_words:
                if i.lower() is j:
                    BAD_WORD =True
        print(output)
        output = output[0]["generated_text"]
        if BAD_WORD == True:
            st.write(i)
            st.write("The bot generated a slur, please try again.")
            BAD_WORD = False
        else:
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
    BAD_WORD = False   
    st.title("Persona Chat")
    st.write("Please enter your message below. First generation may take up to a minute or more, as the model is loading. Latter generations should load faster.")
    
    temperature = st.slider("Temperature", 0.1, 1.0, 0.3, 0.1)
    top_k = st.slider("Top K", 1, 100, 5, 1)
    max_length = st.slider("Max Length", 1, 250, 25, 1)
    do_sample = st.checkbox("Do Sample (If unchecked, will use greedy decoding, which is more coherent)")
  

    user_chat = st.text_input("Chat with Persona!")
    stan_chat_button = st.button("Send")
    st.write("Please only press Send once, it will take a short amount of time to load during the first generation.")
   

    if stan_chat_button:
        
        
        user_chat = "User: " + user_chat
        st.session_state.persona_chat_history.append(user_chat)
        st.write(user_chat)
        user_chat = user_chat + " Bot:"
        output = per_generate(user_chat, max_length=max_length, temperature=temperature, top_k=top_k, do_sample=do_sample)
        check_output = output[0]["generated_text"]
        check_output = check_output.split(" ")
        for i in check_output:
            for j in bad_words:
                if i.lower() is j:
                    BAD_WORD =True
        print(output)

        if BAD_WORD == True:
            st.write("The bot generated a slur, please try again.")
            BAD_WORD = False
        else:
            output = output[0]["generated_text"]
            output = output.split("Bot:")[1]
            output = "Persona: " + output
            st.write(output)


    
        
def gordon_chat():
    BAD_WORD = False
    st.title("Chat with Gordon")
    st.write("Please enter your message below. First generation may take up to a minute or more, as the model is loading. Latter generations should load faster.")
    
    temperature = st.slider("Temperature", 0.1, 1.0, 0.3, 0.1)
    top_k = st.slider("Top K", 1, 100, 5, 1)
    max_length = st.slider("Max Length", 1, 250, 25, 1)
    do_sample = st.checkbox("Do Sample (If unchecked, will use greedy decoding, which is more coherent)")

    user_chat = st.text_input("Chat with Gordon!")
    gordon_chat_button = st.button("Send")    
    st.write("Please only press Send once, it will take a short amount of time to load during the first generation.")

    if gordon_chat_button:
        
        
        user_chat = "User: " + user_chat
        st.session_state.gordon_chat_history.append(user_chat)
        st.write(user_chat)
        user_chat = user_chat + " Bot:"
        output = gor_generate(user_chat, max_length=max_length, temperature=temperature, top_k=top_k, do_sample=do_sample)
        check_output = output[0]["generated_text"]
        check_output = check_output.split(" ")
        for i in check_output:
            for j in bad_words:
                if i.lower() is j:
                    BAD_WORD =True
        print(output)


        if BAD_WORD == True:
            st.write("The bot generated a slur, please try again.")
            BAD_WORD = False
        else:
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