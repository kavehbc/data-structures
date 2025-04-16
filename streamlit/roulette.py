import streamlit as st
import random

def iseven(pick):
    if pick % 2 == 0:
        return True
    return False
    
def main():
    st.title("Roulette Simulator")

    # UI Parameters
    with st.sidebar:
        initial_bet = st.number_input("Initial Bet Value", min_value=1, max_value=100, value=10, step=1) 
        n_rounds = st.slider("\# of Rounds", min_value=1, max_value=1000, value=100, step=1)
        bet_even = st.toggle("Is even")

    # LOGIC
    roulette = []
    for i in range(37):
        roulette.append(i)
    roulette.append("00")

    bet_value = initial_bet
    bets = []
    winnings = []
    
    for i in range(n_rounds):
        random.shuffle(roulette)
        random_index = random.randint(0, len(roulette) - 1)
        pick = roulette[random_index]
        
        bets.append(bet_value)
        if int(pick) == 0:
            # lost
            bet_value *= 2
            # print("Lost")
        elif iseven(int(pick)) == bet_even:
            # win
            bet_value = initial_bet
            winnings.append(initial_bet)
            # print("Win")
        else:
            # lost
            bet_value *= 2
            # print("Lost")

    with st.expander("Details"):
        st.header("Bets")
        st.write(bets)
        st.header("Winings")
        st.write(winnings)

    st.write(f"number of times we win out of {n_rounds}: **{len(winnings)}**")
    st.write(f"total winnings: **{sum(winnings):,} $**")
    st.write(f"maximum bet: **{max(bets):,} $**")
    st.write(f"total money needed: **{(max(bets) * 2) - initial_bet:,} $**")


if __name__ == "__main__":
    main()
    