import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# =========================
# ⭐ 中文修复（最稳定）
# =========================
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="Kobe Shot Dashboard", layout="wide")

df = pd.read_csv("data_cleaned.csv")

st.title("🏀 Kobe Bryant 投篮数据分析")

col1, col2 = st.columns(2)

# =========================
# 1. 投篮分布
# =========================
with col1:
    st.subheader("投篮分布")

    fig, ax = plt.subplots(figsize=(6,6))
    ax.scatter(df["loc_x"], df["loc_y"], s=1, alpha=0.4)

    ax.set_title("Shot Distribution")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # ⭐ 横向显示（你要的）
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)

    st.pyplot(fig)

# =========================
# 2. 区域命中率
# =========================
with col2:
    st.subheader("区域命中率")

    data1 = df.groupby("shot_zone_basic")["shot_made_flag"].mean()

    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(data1.index, data1.values)

    plt.xticks(rotation=0)  # ⭐ 关键：不旋转
    ax.set_ylim(0, 1)

    ax.set_title("Shot Zone FG%")

    st.pyplot(fig)

# =========================
# 3. 距离命中率
# =========================
st.subheader("距离命中率")

data2 = df.groupby("distance_range")["shot_made_flag"].mean()

fig, ax = plt.subplots(figsize=(8,4))
ax.bar(data2.index, data2.values)

plt.xticks(rotation=0)  # ⭐ 横着
ax.set_ylim(0, 1)

ax.set_title("Distance FG%")

st.pyplot(fig)

# =========================
# 4. ⭐ 热力图（改成稳定版）
# =========================
st.subheader("🏀 投篮热力图（球场版）")

fig, ax = plt.subplots(figsize=(8,7))

# 球场图
try:
    court = Image.open("court.png")
    ax.imshow(court, extent=[-250, 250, 0, 470], alpha=0.9)
except:
    st.warning("没有 court.png")

# ⭐ 用 hexbin（稳定 + 清晰）
hb = ax.hexbin(
    df["loc_x"],
    df["loc_y"],
    gridsize=35,
    cmap="Reds",
    alpha=0.6
)

plt.colorbar(hb, ax=ax, label="Shot Density")

ax.set_xlim(-250, 250)
ax.set_ylim(0, 470)

# ⭐ 关键：去掉乱七八糟坐标
ax.set_xticks([])
ax.set_yticks([])

ax.set_title("Kobe Shot Heatmap")

st.pyplot(fig)