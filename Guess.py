import streamlit as st
import random

st.title("🎲 Number Guessing Game")

# Initialize session state
if "number" not in st.session_state:
    st.session_state.number = random.randint(1, 100)
    st.session_state.attempt = 1
    st.session_state.max_attempts = 4
    st.session_state.result = ""

# Show current attempt
st.write(f"Attempt {st.session_state.attempt}/{st.session_state.max_attempts}")

# Get user's guess
guess = st.number_input("Enter your guess (1-100):", min_value=1, max_value=100, step=1)

if st.button("Submit Guess"):
    if st.session_state.attempt <= st.session_state.max_attempts:
        if guess < st.session_state.number:
            st.session_state.result = "Too low ⬇️"
        elif guess > st.session_state.number:
            st.session_state.result = "Too high ⬆️"
        else:
            st.session_state.result = "🎉 Correct! You guessed the number!"
        st.session_state.attempt += 1

    # End of game
    if st.session_state.attempt > st.session_state.max_attempts and guess != st.session_state.number:
        st.session_state.result = f"❌ Out of guesses! The number was {st.session_state.number}."

    st.rerun()

# Display result
if st.session_state.result:
    st.write(st.session_state.result)

# Restart game
if st.button("Restart Game"):
    for key in ["number", "attempt", "max_attempts", "result"]:
        st.session_state.pop(key, None)
    st.rerun()
