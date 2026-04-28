import streamlit as st
import math

st.set_page_config(page_title="Football Model", layout="centered")

st.title("⚽ Live Model (Team + Total)")

st.markdown("### 🟢 Enter FULL MATCH averages")

# --- TEAM INPUTS ---
home_shot = st.number_input("Home Shots", value=12.0)
away_shot = st.number_input("Away Shots", value=11.0)

home_foul = st.number_input("Home Fouls", value=12.0)
away_foul = st.number_input("Away Fouls", value=11.0)

home_corner = st.number_input("Home Corners", value=5.0)
away_corner = st.number_input("Away Corners", value=4.5)

home_throw = st.number_input("Home Throw-ins", value=18.0)
away_throw = st.number_input("Away Throw-ins", value=17.0)

home_card = st.number_input("Home Cards", value=1.5)
away_card = st.number_input("Away Cards", value=1.2)

st.markdown("---")

# --- CONTROLS ---
minutes = st.slider("Interval (minutes)", 1, 10, 1)
match_minute = st.slider("Match minute", 1, 90, 45)
margin = st.slider("Margin (%)", 0, 20, 8) / 100

fh_min = 46.5
sh_min = 48.5

# --- FUNCTIONS ---
def prob(lmbda):
    return 1 - math.exp(-lmbda)

def odds(p, margin):
    if p <= 0:
        return 0
    return (1 / p) * (1 - margin)

def calc_lambda(avg, total_minutes, interval):
    return (avg / total_minutes) * interval

# --- BOOSTS ---
throw_boost = 1 + (minutes / 10) * 0.15

shot_boost = 1
if match_minute >= 75:
    shot_boost = 1 + ((match_minute - 75) / 15) * 0.25

# --- HALF SPLIT ---
def split(avg):
    return avg * 0.48, avg * 0.52

# --- MARKETS ---
markets = {
    "Shots": (home_shot, away_shot, 1.17),
    "Fouls": (home_foul, away_foul, 1.11),
    "Corners": (home_corner, away_corner, 1.15),
    "Throw-ins": (home_throw, away_throw, None),
    "Cards": (home_card, away_card, 2.0),
}

st.subheader(f"📊 Results ({minutes} min window)")

for name, (home, away, adj) in markets.items():

    # --- split halves ---
    fh_home, sh_home = split(home)
    fh_away, sh_away = split(away)

    # --- SH adjustments ---
    if name == "Throw-ins":
        sh_home = fh_home - 0.25
        sh_away = fh_away - 0.25
    else:
        sh_home = fh_home * adj
        sh_away = fh_away * adj

    # --- lambdas ---
    l_home_fh = calc_lambda(fh_home, fh_min, minutes)
    l_home_sh = calc_lambda(sh_home, sh_min, minutes)

    l_away_fh = calc_lambda(fh_away, fh_min, minutes)
    l_away_sh = calc_lambda(sh_away, sh_min, minutes)

    # --- boosts ---
    if name == "Throw-ins":
        l_home_fh *= throw_boost
        l_home_sh *= throw_boost
        l_away_fh *= throw_boost
        l_away_sh *= throw_boost

    if name == "Shots":
        l_home_fh *= shot_boost
        l_home_sh *= shot_boost
        l_away_fh *= shot_boost
        l_away_sh *= shot_boost

    # --- TOTAL ---
    l_total_fh = l_home_fh + l_away_fh
    l_total_sh = l_home_sh + l_away_sh

    # --- probabilities ---
    p_home_fh = prob(l_home_fh)
    p_home_sh = prob(l_home_sh)

    p_away_fh = prob(l_away_fh)
    p_away_sh = prob(l_away_sh)

    p_total_fh = prob(l_total_fh)
    p_total_sh = prob(l_total_sh)

    # --- odds ---
    o_home_fh = odds(p_home_fh, margin)
    o_home_sh = odds(p_home_sh, margin)

    o_away_fh = odds(p_away_fh, margin)
    o_away_sh = odds(p_away_sh, margin)

    o_total_fh = odds(p_total_fh, margin)
    o_total_sh = odds(p_total_sh, margin)

    # --- OUTPUT ---
    st.markdown(f"### {name}")

    st.write("🏠 Home")
    st.write(f"FH → {round(p_home_fh*100,1)}% | Odds: {round(o_home_fh,2)}")
    st.write(f"SH → {round(p_home_sh*100,1)}% | Odds: {round(o_home_sh,2)}")

    st.write("🚗 Away")
    st.write(f"FH → {round(p_away_fh*100,1)}% | Odds: {round(o_away_fh,2)}")
    st.write(f"SH → {round(p_away_sh*100,1)}% | Odds: {round(o_away_sh,2)}")

    st.write("🌍 TOTAL")
    st.write(f"FH → {round(p_total_fh*100,1)}% | Odds: {round(o_total_fh,2)}")
    st.write(f"SH → {round(p_total_sh*100,1)}% | Odds: {round(o_total_sh,2)}")

    st.markdown("---")
