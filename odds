import streamlit as st
import math

st.set_page_config(page_title="Live Football Model", layout="centered")

st.title("⚽ Live Probability Calculator")

st.write("შეიყვანე პირველი ტაიმის საშუალოები (FH avg)")

# --- INPUTS ---
X_throw = st.number_input("Throw-ins (FH)", value=16.0)
X_foul = st.number_input("Fouls (FH)", value=10.1)
X_shot = st.number_input("Shots (FH)", value=13.9)
X_sot = st.number_input("Shots on Target (FH)", value=5.85)
X_off = st.number_input("Offside (FH)", value=2.05)
X_gk = st.number_input("Goal Kick (FH)", value=7.25)
X_corner = st.number_input("Corner (FH)", value=4.5)
X_card = st.number_input("Cards (FH)", value=1.35)

st.markdown("---")

# --- SETTINGS ---
minutes = st.slider("აირჩიე წუთები", 1, 10, 1)
margin = st.slider("Margin (%)", 0, 20, 8) / 100

fh_min = 46.5
sh_min = 48.5

# --- FUNCTIONS ---
def prob(lmbda):
    return 1 - math.exp(-lmbda)

def odds(p, margin):
    if p == 0:
        return 0
    return (1 / p) * (1 - margin)

def calc_lambda(avg, total_minutes, interval):
    return (avg / total_minutes) * interval

# --- SECOND HALF RULES ---
data = {
    "Throw-in": (X_throw, X_throw - 0.5),
    "Foul": (X_foul, X_foul * 1.11),
    "Shot": (X_shot, X_shot * 1.17),
    "Shot on Target": (X_sot, X_sot * 1.14),
    "Offside": (X_off, X_off),
    "Goal Kick": (X_gk, X_gk * 1.07),
    "Corner": (X_corner, X_corner * 1.15),
    "Card": (X_card, X_card * 2),
}

st.subheader(f"📊 შედეგები ({minutes} წუთში)")

for market, (fh, sh) in data.items():

    # lambdas
    l_fh = calc_lambda(fh, fh_min, minutes)
    l_sh = calc_lambda(sh, sh_min, minutes)

    # probabilities
    p_fh = prob(l_fh)
    p_sh = prob(l_sh)

    # odds
    o_fh = odds(p_fh, margin)
    o_sh = odds(p_sh, margin)

    st.markdown(f"### {market}")
    st.write(f"FH → {round(p_fh*100,1)}% | Odds: {round(o_fh,2)}")
    st.write(f"SH → {round(p_sh*100,1)}% | Odds: {round(o_sh,2)}")

    st.markdown("---")
