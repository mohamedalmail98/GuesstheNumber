import streamlit as st
import random
import pandas as pd
import os

# ---------- Configuration ----------
MAX_ATTEMPTS = 4
PASSWORD = "letmein123"  # Change this to your own admin password
WINNERS_LOG = "winners_log.csv"

# ---------- Persistent Winner Storage ----------
def save_winner_name(name):
    if os.path.exists(WINNERS_LOG):
        df = pd.read_csv(WINNERS_LOG)
        if name not in df["Winner"].values:
            df = pd.concat([df, pd.DataFrame([{"Winner": name}])], ignore_index=True)
            df.to_csv(WINNERS_LOG, index=False)
    else:
        df = pd.DataFrame([{"Winner": name}])
        df.to_csv(WINNERS_LOG, index=False)

# ---------- Streamlit Session Initialization ----------
if 'target' not in st.session_state:
    st.session_state.target = random.randint(1, 20)
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

st.title("🎯 Guess the Number Game!")

# ---------- Player Input ----------
name = st.text_input("Enter your name:")

if name and not st.session_state.game_over:
    guess = st.number_input("Guess a number between 1 and 20:", min_value=1, max_value=20, step=1)
    if st.button("Submit Guess"):
        st.session_state.attempts += 1

        if guess == st.session_state.target:
            st.success(f"🎉 Congrats {name}! You guessed the correct number!")
            save_winner_name(name)
            st.session_state.game_over = True
        elif st.session_state.attempts >= MAX_ATTEMPTS:
            st.error(f"❌ Game over! You've used all {MAX_ATTEMPTS} attempts. The number was {st.session_state.target}.")
            st.session_state.game_over = True
        else:
            if guess < st.session_state.target:
                st.warning(f"❗ Too low! Try a higher number. Attempts left: {MAX_ATTEMPTS - st.session_state.attempts}")
            else:
                st.warning(f"❗ Too high! Try a lower number. Attempts left: {MAX_ATTEMPTS - st.session_state.attempts}")

# ---------- Admin Panel ----------
with st.expander("🔐 Admin Access"):
    password = st.text_input("Enter admin password", type="password")
    if password == 'letmein123':
        st.success("✅ Admin access granted.")
        if os.path.exists(WINNERS_LOG):
            df = pd.read_csv(WINNERS_LOG)
            st.subheader("🏆 All-Time Winners:")
            st.write(df)
if st.button("🗑️ Clear Winners Log"):
    if os.path.exists(WINNERS_LOG):
        os.remove(WINNERS_LOG)
        st.success("Winners log has been cleared.")
    else:
        st.info("No winners log file to delete.")

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Winners CSV", data=csv, file_name="winners_log.csv", mime="text/csv")
        else:
            st.info("No winners recorded yet.")
    elif password:
        st.error("❌ Incorrect password.")





# ---------- Restart Game ----------
if st.session_state.game_over:
    if st.button("🔁 Restart Game"):
        st.session_state.target = random.randint(1, 20)
        st.session_state.attempts = 0
        st.session_state.game_over = False










