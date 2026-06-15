import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

st.set_page_config(page_title="Kobe Shot Dashboard", layout="wide")

df = pd.read_csv("data_cleaned.csv")

st.title("🏀 Kobe Bryant 投篮数据分析")

col1, col2 = st.columns(2)

# =========================
# 1. 投篮分布（保留）
# =========================
with col1:
    st.subheader("投篮分布")

    fig, ax = plt.subplots(figsize=(6,6))
    ax.scatter(df["loc_x"], df["loc_y"], s=1, alpha=0.5)

    ax.set_title("Shot Distribution")
    ax.set_xlabel("Court X")
    ax.set_ylabel("Court Y")

    plt.xticks(rotation=0)
    plt.yticks(rotation=0)

    st.pyplot(fig)

# =========================
# 2. 区域命中率（保留）
# =========================
with col2:
    st.subheader("区域命中率")

    data1 = df.groupby("shot_zone_basic")["shot_made_flag"].mean()

    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(data1.index, data1.values)

    plt.xticks(rotation=30, ha='right')
    ax.set_ylim(0, 1)

    ax.set_title("Shot Zone FG%")

    st.pyplot(fig)

# =========================
# 3. 距离命中率（保留）
# =========================
st.subheader("距离命中率")

data2 = df.groupby("distance_range")["shot_made_flag"].mean()

fig, ax = plt.subplots(figsize=(8,4))
ax.bar(data2.index, data2.values)

plt.xticks(rotation=30, ha='right')
ax.set_ylim(0, 1)

ax.set_title("Distance FG%")

st.pyplot(fig)

# =========================
# 4. 🏀 球场热力图（新增）
# =========================
st.subheader("🏀 投篮热力图（Shot Heatmap）")

fig, ax = plt.subplots(figsize=(8,7))

# 球场背景
try:
    court = Image.open("court.png")
    ax.imshow(court, extent=[-250, 250, 0, 470], alpha=0.5)
except:
    st.warning("未找到 court.png，仅显示热力图")

# 热力图
hb = ax.hexbin(
    df["loc_x"],
    df["loc_y"],
    C=df["shot_made_flag"],
    reduce_C_function=np.mean,
    gridsize=30,
    cmap="Reds",
    alpha=0.7
)

cb = plt.colorbar(hb, ax=ax, shrink=0.8)
cb.set_label("FG%")

ax.set_xlim(-250, 250)
ax.set_ylim(0, 470)

ax.set_xticks([])
ax.set_yticks([])

ax.set_title("Kobe Shot Heatmap")

st.pyplot(fig)