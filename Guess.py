import streamlit as st
import random

# Initialize session state variables
if 'target' not in st.session_state:
    st.session_state.target = random.randint(1, 20)
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'players' not in st.session_state:
    st.session_state.players = []
if 'winners' not in st.session_state:
    st.session_state.winners = []

st.title("🎯 Guess the Number Game!")

# Input for player name
name = st.text_input("Enter your name:")

# Allow input only if name is entered and game isn't over
if name:
    guess = st.number_input("Guess a number between 1 and 20:", min_value=1, max_value=20, step=1)
    if st.button("Submit Guess") and not st.session_state.game_over:
        st.session_state.attempts += 1
        st.session_state.players.append(name)

        if guess == st.session_state.target:
            st.success(f"🎉 Congrats {name}! You guessed the correct number!")
            st.session_state.winners.append(name)
            st.session_state.game_over = True
        elif st.session_state.attempts >= 4:
            st.error(f"❌ Game over! You've used all attempts. The number was {st.session_state.target}.")
            st.session_state.game_over = True
        else:
            st.info(f"Wrong guess, try again! Attempts left: {4 - st.session_state.attempts}")

# Show results after game ends
if st.session_state.game_over:
    st.subheader("📋 Players who tried the game:")
    st.write(set(st.session_state.players))

    st.subheader("🏆 Winners:")
    if st.session_state.winners:
        st.write(st.session_state.winners)
    else:
        st.write("No one won this time!")

    if st.button("Restart Game"):
        st.session_state.target = random.randint(1, 20)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.players = []
        st.session_state.winners = []
