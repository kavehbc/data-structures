import streamlit as st
import random
    
def main():
    st.title("Guessing Game")
    max_value = st.number_input("Enter maximum number", value=500, min_value=1, step=1)
    your_guess = st.number_input("Enter your guess", value=None, min_value=1, max_value=max_value, step=1)

    if "max" in st.session_state:
        if int(st.session_state["max"]) != int(max_value):
            del st.session_state["chosen"]
            
    if "chosen" not in st.session_state:
        chosen_number = random.randint(1, max_value)
        st.session_state["chosen"] = chosen_number
        st.session_state["max"] = max_value
        counter = 0
        st.session_state["counter"] = counter
    else:
        chosen_number = st.session_state["chosen"]
        st.session_state["counter"] += 1
        counter = st.session_state["counter"]
        
    # st.write(chosen_number)
    # st.write(st.session_state["max"])

    if your_guess is not None:
        if your_guess == chosen_number:
            st.success(f"**Huuray!** That's correct with {counter} guesses")
            st.balloons()
            del st.session_state["chosen"]
        elif your_guess < chosen_number:
            st.info(f"Trial #{counter}: My number is **higher**!")
        elif your_guess > chosen_number:
            st.info(f"Trial #{counter}: My number is **lower**!")
        
if __name__ == "__main__":
    main()
    