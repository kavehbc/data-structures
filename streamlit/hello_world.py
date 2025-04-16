import streamlit as st
import pandas as pd

def main():
    st.title("Hello World")
    st.write("Hello Test")

    name = st.sidebar.text_input("What is your name?")
    st.sidebar.write(name)

    data = {"A": [1, 2, 3],
            "B": [4, 5, 6]}
    st.write(data)

    df = pd.DataFrame(data)
    st.write(df)

    new_df = st.data_editor(df)

    btn_ok = st.button("OK")
    if btn_ok:
        st.write("Clicked")


if __name__ == "__main__":
    main()
    