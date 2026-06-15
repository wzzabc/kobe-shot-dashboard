import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Kobe Shot Dashboard", layout="wide")

df = pd.read_csv("data_cleaned.csv")

st.title("🏀 Kobe Bryant 投篮数据分析")

col1, col2 = st.columns(2)

with col1:
    st.subheader("投篮分布")
    fig, ax = plt.subplots()
    ax.scatter(df["loc_x"], df["loc_y"], s=1)
    st.pyplot(fig)

with col2:
    st.subheader("区域命中率")
    st.bar_chart(df.groupby("shot_zone_basic")["shot_made_flag"].mean())

st.subheader("距离命中率")
st.bar_chart(df.groupby("distance_range")["shot_made_flag"].mean())