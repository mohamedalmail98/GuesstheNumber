import streamlit as st
import random
import pandas as pd

# Initialize session state
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

# Name input for player
name = st.text_input("Enter your name:")

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
            if guess < st.session_state.target:
                st.warning(f"❗ Too low! Try a higher number. Attempts left: {4 - st.session_state.attempts}")
            else:
                st.warning(f"❗ Too high! Try a lower number. Attempts left: {4 - st.session_state.attempts}")

# Admin-only view (secret password box)
with st.expander("🔐 Admin Access"):
    password = st.text_input("Enter admin password", type="password")
    if password == "letmein123":  # change this to your own secret password
        st.success("Admin access granted.")
        st.subheader("📋 All Players:")
        st.write(st.session_state.players)
        st.subheader("🏆 Winners:")
        st.write(list(set(st.session_state.players)))
        
        unique_players = list(set(st.session_state.players))
        df = pd.DataFrame({
    "Player": unique_players,
    "Winner": [name if name in st.session_state.winners else "" for name in unique_players]
})
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Players CSV", data=csv, file_name="players.csv", mime="text/csv")
    elif password:
        st.error("Incorrect password.")

# Restart the game
if st.session_state.game_over:
    if st.button("Restart Game"):
        st.session_state.target = random.randint(1, 20)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.players = []
        st.session_state.winners = []

import smtplib
from email.message import EmailMessage

def notify_admin(name):
    msg = EmailMessage()
    msg.set_content(f"🎮 A new player just tried your game: Guess the Number")
    msg["Subject"] = "New Game Attempt"
    msg["From"] = "mohammeda.almail@gmail.com"
    msg["To"] = "mohammeda.almail@gmail.com"

    # Replace below with your real credentials (or better: use environment variables)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "mohammeda.almail@gmail.com"
    sender_password = "kanoon7787"

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
    except Exception as e:
        st.warning(f"Could not send email: {e}")

