import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import numpy as np

# =========================
# 必须只写一次（放最顶部）
# =========================
st.set_page_config(page_title="Kobe Shot Dashboard", layout="wide")

# =========================
# 读取数据（只读一次）
# =========================
df = pd.read_csv("data_cleaned.csv")

# =========================
# 数据清洗 & 统一半场坐标
# =========================
df_clean = df.dropna(subset=["loc_x", "loc_y", "shot_made_flag"])
df_clean = df_clean[
    (df_clean["loc_x"].between(-250, 250)) &
    (df_clean["loc_y"].between(0, 470))
]

st.title("🏀 Kobe Bryant 投篮数据分析")

# =========================
# 球场绘制函数（半场）
# =========================
def draw_court(ax):

    hoop = Circle((0, 0), 7.5, linewidth=2, color="orange", fill=False)
    ax.add_patch(hoop)

    ax.add_patch(Rectangle((-80, 0), 160, 190, fill=False, linewidth=2))

    ax.add_patch(Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=2))

    ax.plot([-250, 250], [470, 470], color="black", linewidth=2)

    return ax


# =========================
# 左右图
# =========================
col1, col2 = st.columns(2)

# ===== 投篮分布（修复版）=====
with col1:
    st.subheader("投篮分布（半场）")

    fig, ax = plt.subplots(figsize=(5, 5))
    ax = draw_court(ax)

    ax.scatter(
        df_clean["loc_x"],
        df_clean["loc_y"],
        s=2,
        alpha=0.4
    )

    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)
    ax.set_xticks([])
    ax.set_yticks([])

    st.pyplot(fig)


# ===== 区域命中率 =====
with col2:
    st.subheader("区域命中率")

    st.bar_chart(
        df_clean.groupby("shot_zone_basic")["shot_made_flag"].mean()
    )

# =========================
# 距离命中率
# =========================
st.subheader("距离命中率")

st.bar_chart(
    df_clean.groupby("distance_range")["shot_made_flag"].mean()
)

# =========================
# 热力图（稳定版）
# =========================
st.subheader("投篮热力图（FG%）")

fig, ax = plt.subplots(figsize=(6, 6))
ax = draw_court(ax)

hb = ax.hexbin(
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

plt.colorbar(hb, ax=ax, label="FG%")

ax.set_xlim(-250, 250)
ax.set_ylim(0, 470)
ax.set_aspect("equal")

ax.set_xticks([])
ax.set_yticks([])

st.pyplot(fig)