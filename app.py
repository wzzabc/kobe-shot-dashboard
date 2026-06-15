import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib as mpl

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

# 球场背景 + 命中率热力图
# =========================
st.subheader("📍 投篮位置命中率（Shot Probability Map）")

fig, ax = plt.subplots(figsize=(8,7))

# 1. 加载球场图片
court = Image.open("court.png")
ax.imshow(court, extent=[-250, 250, 0, 470])

# 2. 计算命中率（简单版：用 scatter + 透明度模拟）
# 方法：用 hexbin 计算局部命中率

hb = ax.hexbin(
    df["loc_x"],
    df["loc_y"],
    C=df["shot_made_flag"],
    reduce_C_function=np.mean,
    gridsize=30,
    cmap="Reds",
    alpha=0.7
)

cb = plt.colorbar(hb, ax=ax)
cb.set_label("Shot FG%")

ax.set_xlim(-250, 250)
ax.set_ylim(0, 470)

ax.set_xticks([])
ax.set_yticks([])

ax.set_title("Kobe Bryant Shot Accuracy Heatmap")

st.pyplot(fig)