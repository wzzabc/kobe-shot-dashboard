import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import numpy as np

st.set_page_config(page_title="Kobe Shot Dashboard", layout="wide")

st.title("🏀 Kobe Bryant 投篮数据分析（完整版）")

# =========================
# 数据
# =========================
df = pd.read_csv("data_cleaned.csv")
df_clean = df.dropna(subset=["loc_x", "loc_y", "shot_made_flag"])

# =========================================================
# 1️⃣ 投篮分布（Scatter）
# =========================================================
st.subheader("📍 投篮分布图")

fig1, ax1 = plt.subplots()

ax1.scatter(
    df_clean["loc_x"],
    df_clean["loc_y"],
    s=2,
    alpha=0.5,
    c="blue"
)

ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_title("Shot Distribution")

st.pyplot(fig1)

# =========================================================
# 2️⃣ 热力图（Hexbin）
# =========================================================
st.subheader("🔥 投篮热力图（命中率）")

fig2, ax2 = plt.subplots(figsize=(6, 6))

hb = ax2.hexbin(
    df_clean["loc_x"],
    df_clean["loc_y"],
    C=df_clean["shot_made_flag"],
    reduce_C_function=np.mean,
    gridsize=30,
    cmap="Reds",
    mincnt=1,
    vmin=0,
    vmax=1,
    alpha=0.85
)

plt.colorbar(hb, ax=ax2, label="FG%")

ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_title("Shot Heatmap (FG%)")

st.pyplot(fig2)

# =========================================================
# 3️⃣ 区域命中率
# =========================================================
st.subheader("🎯 区域命中率")

zone_fg = df_clean.groupby("shot_zone_basic")["shot_made_flag"].mean()

fig3, ax3 = plt.subplots()
zone_fg.sort_values().plot(kind="bar", ax=ax3)

ax3.set_ylim(0, 1)
ax3.set_ylabel("FG%")

st.pyplot(fig3)

# =========================================================
# 4️⃣ 距离命中率
# =========================================================
st.subheader("📏 距离命中率")

dist_fg = df_clean.groupby("distance_range")["shot_made_flag"].mean()

fig4, ax4 = plt.subplots()
dist_fg.plot(kind="bar", ax=ax4, color="orange")

ax4.set_ylim(0, 1)
ax4.set_ylabel("FG%")

st.pyplot(fig4)

# =========================================================
# 5️⃣ 半场球场 + 投篮分布
# =========================================================
st.subheader("🏀 半场投篮（带球场）")

def draw_court(ax):

    hoop = Circle((0, 0), 7.5, linewidth=2, color="orange", fill=False)
    ax.add_patch(hoop)

    ax.add_patch(Rectangle((-80, 0), 160, 190, fill=False, linewidth=2))

    ax.add_patch(Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=2))

    ax.plot([-250, 250], [0, 0], color="black", linewidth=2)

    return ax


fig5, ax5 = plt.subplots(figsize=(8, 7))
ax5 = draw_court(ax5)

ax5.scatter(
    df_clean["loc_x"],
    df_clean["loc_y"],
    s=2,
    alpha=0.35,
    c="blue"
)

ax5.set_xlim(-250, 250)
ax5.set_ylim(0, df_clean["loc_y"].max() + 10)

ax5.set_aspect("equal")

ax5.set_xticks([])
ax5.set_yticks([])

ax5.set_title("Half Court Shot Map")

st.pyplot(fig5)