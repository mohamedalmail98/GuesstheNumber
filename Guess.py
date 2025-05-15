import streamlit as st
import random
import pandas as pd
import os

# ---------- Configuration ----------
MAX_ATTEMPTS = 4
PASSWORD = "letmein7787"
WINNERS_LOG = "winners_log.csv"
PLAYERS_LOG = "players_log.csv"

# ---------- Save to Players Log ----------
def log_player(name, result):
    entry = pd.DataFrame([{"Player": name, "Result": result}])
    if os.path.exists(PLAYERS_LOG):
        df = pd.read_csv(PLAYERS_LOG)
        df = pd.concat([df, entry], ignore_index=True)
    else:
        df = entry
    df.to_csv(PLAYERS_LOG, index=False)

# ---------- Save to Winners Log ----------
def save_winner_name(name):
    if os.path.exists(WINNERS_LOG):
        df = pd.read_csv(WINNERS_LOG)
        if name not in df["Winner"].values:
            df = pd.concat([df, pd.DataFrame([{"Winner": name}])], ignore_index=True)
            df.to_csv(WINNERS_LOG, index=False)
    else:
        df = pd.DataFrame([{"Winner": name}])
        df.to_csv(WINNERS_LOG, index=False)

# ---------- Initialize Session State ----------
if 'target' not in st.session_state:
    st.session_state.target = random.randint(1, 20)
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'logged' not in st.session_state:
    st.session_state.logged = False

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
            log_player(name, "Won")
            st.session_state.game_over = True
        elif st.session_state.attempts >= MAX_ATTEMPTS:
            st.error(f"❌ Game over! You've used all {MAX_ATTEMPTS} attempts. The number was {st.session_state.target}.")
            log_player(name, "Lost")
            st.session_state.game_over = True
        else:
            if guess < st.session_state.target:
                st.warning(f"❗ Too low! Try a higher number. Attempts left: {MAX_ATTEMPTS - st.session_state.attempts}")
            else:
                st.warning(f"❗ Too high! Try a lower number. Attempts left: {MAX_ATTEMPTS - st.session_state.attempts}")

# ---------- Admin Panel ----------
with st.expander("🔐 Admin Access"):
    password = st.text_input("Enter admin password", type="password", key="admin_password_input")

    if password == 'letmein7787':
        st.success("✅ Admin access granted.")

        # Winners Log
        if os.path.exists(WINNERS_LOG):
            df_winners = pd.read_csv(WINNERS_LOG)
            st.subheader("🏆 All-Time Winners:")
            st.dataframe(df_winners)

            csv = df_winners.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Winners CSV", data=csv, file_name="winners_log.csv", mime="text/csv")

            selected_winner = st.selectbox("Select a winner to delete", df_winners["Winner"].unique(), key="delete_winner_dropdown")
            if st.button("❌ Delete Selected Winner"):
                df_winners = df_winners[df_winners["Winner"] != selected_winner]
                df_winners.to_csv(WINNERS_LOG, index=False)
                st.success(f"✅ Winner '{selected_winner}' has been removed.")
                st.stop()

            st.warning("🧹 This will permanently clear all winner records.")
            if st.button("🧹 Clear All Winners"):
                pd.DataFrame(columns=["Winner"]).to_csv(WINNERS_LOG, index=False)
                st.success("✅ Winners log has been cleared.")
                st.stop()
        else:
            st.info("No winners recorded yet.")

        # Players Log
        st.markdown("---")
        if os.path.exists(PLAYERS_LOG):
            df_players = pd.read_csv(PLAYERS_LOG)
            st.subheader("🧑‍💻 All Players (Winners and Losers):")
            st.dataframe(df_players)

            csv_players = df_players.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Players CSV", data=csv_players, file_name="players_log.csv", mime="text/csv")

            st.warning("🧹 This will clear all player history.")
            if st.button("🧹 Clear All Player Records"):
                pd.DataFrame(columns=["Player", "Result"]).to_csv(PLAYERS_LOG, index=False)
                st.success("✅ Player log has been cleared.")
                st.stop()
        else:
            st.info("No players recorded yet.")

    elif password:
        st.error("❌ Incorrect password.")

# ---------- Restart Game ----------
if st.session_state.game_over:
    if st.button("🔁 Restart Game"):
        st.session_state.target = random.randint(1, 20)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.logged = False












