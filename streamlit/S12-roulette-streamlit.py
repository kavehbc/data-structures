import streamlit as st
import random


def roll(roulette):
    random_index = random.randint(0, len(roulette) - 1)
    random_pick = roulette[random_index]

    if int(random_pick) == 0:
        is_even = None
    else:
        if int(random_pick) % 2 == 0:
            is_even = True
        else:
            is_even = False
            
    return random_pick, is_even


st.title("Roulette")

# initializing roulette wheel
roulette = [str(i) for i in range(1,37)]
roulette.append('0')
roulette.append('00')
random.shuffle(roulette)
# st.write(roulette)

my_pick_is_even = st.sidebar.checkbox("Is Even", value=True)
initial_bet = st.sidebar.number_input("Initial bet", min_value=1, value=20, step=1)
iterations = st.sidebar.number_input("Iterations", min_value=1, value=50, step=1)

my_bets = []
my_rewards = []

current_bet = initial_bet

for i in range(iterations):
    my_bets.append(current_bet)
    random_pick, is_even = roll(roulette)
    
    if is_even == my_pick_is_even:
        # I won
        my_rewards.append(current_bet * 2)
        current_bet = initial_bet
    else:
        # I lose
        current_bet *= 2

# st.subheader("My Bets")
# st.write(my_bets)

# st.subheader("My Rewards")
# st.write(my_rewards)

max_spent = (max(my_bets) * 2) - initial_bet
st.subheader("Max Money Required")
st.write(max_spent)

final_gain = sum(my_rewards) - sum(my_bets)
st.subheader("Final Profit")
st.write(final_gain)

st.line_chart(my_bets)
st.line_chart(my_rewards)