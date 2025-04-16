import streamlit as st
import random
import numpy as np

def check_rows(board):
    for i in range(len(board)):
        row = list(set(board[i]))
        if len(row) == 1 and "_" not in row:
            winner = row[0]
            return winner
    return None

def check_diag(board):
    diag = []
    for i in range(len(board)):
        diag.append(board[i][i])
    diag = list(set(diag))
    if len(diag) == 1 and "_" not in diag:
        winner = diag[0]
        return winner
    return None

def check_winner():
    board = st.session_state["board"]
    winner = check_rows(board)
    if winner is None:
        winner = check_diag(board)
        if winner is None:
            # board = np.array(board).T.tolist()
            board = np.rot90(board).tolist()
            winner = check_rows(board)
            if winner is None:
                winner = check_diag(board)
    return winner

def button_clicked(i, j, mode):
    current_player = st.session_state["current"]
        
    st.session_state["board"][i][j] = current_player
    winner = check_winner()
    if winner is not None:
        st.success(f"Winner is {winner}")
    
    if mode == "Random" and current_player == "X":
        (i, j) = random_play()
        if i is not None:
            st.session_state["current"] = "O"
            button_clicked(i, j, mode)
    else:        
        if current_player == "X":
            st.session_state["current"] = "O"
        else:
            st.session_state["current"] = "X"

def random_play():
    board = st.session_state["board"]
    available = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "_":
                available.append((i, j))

    if len(available) > 0:
        random_index = random.randint(0, len(available) - 1)
        return available[random_index]
    return (None, None)

def reset():
    st.session_state["board"] = [["_", "_", "_"],
                                 ["_", "_", "_"],
                                 ["_", "_", "_"]]
    st.session_state["current"] = "X"

def main():
    st.title("Tic-Tac-Toe")

    if "board" not in st.session_state:
        reset()

    mode = st.sidebar.selectbox("Mode", options=["Manual", "Random"])
                          
    if st.sidebar.button("Reset"):
        reset()

    for i_row, row in enumerate(range(3)):
        cols = st.columns(3)
        for i_col, col in enumerate(cols):
            value = str(st.session_state["board"][i_row][i_col])
            col.button(value, key=f"btn_{i_row}_{i_col}",
                      on_click=button_clicked,
                      args=(i_row, i_col, mode),
                      disabled=(False if value == "_" else True))


    

if __name__ == "__main__":
    main()
