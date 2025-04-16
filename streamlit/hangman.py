import streamlit as st
import random

def main():
    st.title("Hangman")
    words = ["hello", "world"]

    hangman_placeholder = st.empty()
    
    letter = st.text_input("Enter your letter", value="", max_chars=1).lower()

    if "word" not in st.session_state:
        rand_index = random.randint(0, len(words) - 1)
        word = words[rand_index]
        st.session_state["word"] = word
        st.session_state["correct_letters"] = []
        st.session_state["incorrect_letters"] = []
    else:
        word = st.session_state["word"]
        
    # st.write(word)

    if letter in word:
        st.info("Yup!")
        st.session_state["correct_letters"].append(letter)
    else:
        st.error("No!")
        st.session_state["incorrect_letters"].append(letter)
        
    hangman = ""
    for character in word:
        if character in st.session_state["correct_letters"]:
            hangman += character + " "
        else:
            hangman += " \_ "
        
    hangman_placeholder.header(hangman)

    st.subheader("Incorrect Guesses")
    st.write(", ".join(st.session_state["incorrect_letters"]))
    
if __name__ == "__main__":
    main()
    