import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import numpy as np
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

st.set_page_config(page_title="Kobe Heatmap", layout="wide")

df = pd.read_csv("data_cleaned.csv")

st.title("🏀 Kobe Shot Heatmap (Half Court)")

# =========================
# NBA 半场球场
# =========================
def draw_court(ax=None):
    if ax is None:
        ax = plt.gca()

    # 篮筐
    hoop = Circle((0, 0), radius=7.5, linewidth=2, color="orange", fill=False)
    ax.add_patch(hoop)

    # 罚球区
    ax.add_patch(Rectangle((-80, 0), 160, 190, fill=False))

    # 三分线（简化）
    ax.add_patch(Arc((0, 0), 475, 475, theta1=22, theta2=158))

    # 半场边界
    ax.plot([-250, 250], [470, 470], 'k-')

    return ax


# =========================
# Half Court Heatmap (FIXED)
# =========================

fig, ax = plt.subplots(figsize=(8, 7))

# 画球场（你原来的函数）
ax = draw_court(ax)

# -------------------------
# 数据
# -------------------------
x = df["loc_x"].values
y = df["loc_y"].values
z = df["shot_made_flag"].values  # 0/1

# -------------------------
# 🔥关键修复1：分箱热力图
# 用 counts + mean FG%
# -------------------------
hb = ax.hexbin(
    x, y,
    C=z,
    reduce_C_function=np.mean,
    gridsize=30,        # 不要太大，不然糊
    cmap="Reds",
    mincnt=2,           # 至少2个样本才显示
    vmin=0.0,
    vmax=1.0,
    alpha=0.85
)

# -------------------------
# colorbar
# -------------------------
cbar = plt.colorbar(hb, ax=ax)
cbar.set_label("FG%")

# -------------------------
# 🔥关键修复2：NBA半场比例
# -------------------------
ax.set_xlim(-250, 250)
ax.set_ylim(0, 470)
ax.set_aspect("equal")

# -------------------------
# 🔥关键修复3：不要乱转字体
# -------------------------
ax.set_xticks([])
ax.set_yticks([])

ax.set_title("Kobe Bryant Shot Heatmap (Half Court FG%)")

plt.tight_layout()
plt.show()