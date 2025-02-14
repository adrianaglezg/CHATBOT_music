import json
import nltk 
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langdetect import detect
import threading


path_feature_database = 'data/all_extracted_features.json'
with open(path_feature_database, "r", encoding="utf-8") as file:
    corpus_data = json.load(file)



#extracts the preprocessed texts from the corpus to maintain the reference to their features
corpus_texts = []
corpus_features = []  

for entry in corpus_data:
    for key in entry:
        if key.startswith("text_"):  
            corpus_texts.append(entry[key]) 

for entry in corpus_data:
    for key in entry:
        if key.startswith("features_"):  
            corpus_features.append(entry[key])
          


#preprocess

lemmatizer = nltk.stem.WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def preprocess_text(text):
    ''' 
    tokenizes, removes punctuation and lemmatizes
    '''
    tokens = nltk.word_tokenize(text.lower().translate(remove_punct_dict))
    return " ".join(lemmatizer.lemmatize(token) for token in tokens)


vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus_texts)

def chatbot_response(user_input, features= corpus_features):
    ''' 
    response based on cosine similarity
    '''   

    processed_input = preprocess_text(user_input)

    user_vector = vectorizer.transform([processed_input])

    similarities = cosine_similarity(user_vector, tfidf_matrix)

    # find best index to return the features
    best_match_idx = np.argmax(similarities)
    best_match_features = features[best_match_idx]

    return best_match_features


# timeout = 10  # Tiempo límite en segundos
# stop_event = threading.Event()  # Evento para controlar el tiempo de espera

# def countdown_timer():
#     """Función que espera el tiempo límite y termina el programa si no hay input."""
#     global stop_event
#     while not stop_event.wait(timeout):
#         print("\n🕑 Timeout reached! No input received. Exiting...")
#         exit()


# timer_thread = threading.Thread(target=countdown_timer, daemon=True)
# timer_thread.start()
import time



while True:
    time.sleep(2)
    user_input = input("\n👤 Share how you're feeling or what's on your mind (or type 'exit' to close this session): ")

    # stop_event.set()
    # stop_event.clear() #restart

    print(f"\n👤💬 {user_input} ")

    if user_input.lower() == "exit":
        print("\n👋🤖 good bye!")
        break

    elif user_input.lower().replace(" ", "") == "thankyou":
        print("\n🤖 You'r wellcome")
        break
        
    elif user_input.replace(" ", "") == "":
        continue

    try:
        

        language = detect(user_input)  
        if language != "en":
            print("\n🤖❌ Sorry, I can't understand your text. It must be written in English.")
            continue  
        
        print("\n🤖 We are processing your feelings to return the best musical match for you... ⏳")
        response = chatbot_response(user_input)
        print("\n🤖 here it is!. \nThis are the features that have been considered the most accurate for your text:\n")
        # print(json.dumps(response, indent=4, ensure_ascii=False))
        print(json.dumps(response, ensure_ascii=False).replace("\\n", "\n").replace('\\', ""))
        print('hope it helped :)')
        # break


            
    except:
        print("\n🤖❌ Sorry, I couldn't detect the language of your text. Please try again.")

    # if stop_event.is_set(): 
    #         break