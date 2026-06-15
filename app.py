import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# ====== 解决中文显示问题 ======
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 中文
plt.rcParams["axes.unicode_minus"] = False    # 负号正常

st.set_page_config(page_title="Kobe Shot Dashboard", layout="wide")

df = pd.read_csv("data_cleaned.csv")

st.title("🏀 Kobe Bryant 投篮数据分析")

col1, col2 = st.columns(2)

# =========================
# 1. 投篮分布
# =========================
with col1:
    st.subheader("投篮分布")

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(df["loc_x"], df["loc_y"], s=2, alpha=0.4)

    ax.set_title("投篮分布")
    ax.set_xlabel("X坐标")
    ax.set_ylabel("Y坐标")

    # ❗全部保持横着
    ax.tick_params(axis='x', labelrotation=0)
    ax.tick_params(axis='y', labelrotation=0)

    st.pyplot(fig)


# =========================
# 2. 区域命中率
# =========================
with col2:
    st.subheader("区域命中率")

    data1 = df.groupby("shot_zone_basic")["shot_made_flag"].mean()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(data1.index, data1.values)

    ax.set_ylim(0, 1)
    ax.set_title("区域命中率")

    # ❗字体横着（关键修复）
    ax.tick_params(axis='x', labelrotation=0)

    st.pyplot(fig)


# =========================
# 3. 距离命中率
# =========================
st.subheader("距离命中率")

data2 = df.groupby("distance_range")["shot_made_flag"].mean()

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(data2.index, data2.values)

ax.set_ylim(0, 1)
ax.set_title("距离命中率")

ax.tick_params(axis='x', labelrotation=0)

st.pyplot(fig)


# =========================
# 4. 球场热力图（正确版本）
# =========================
st.subheader("🏀 投篮热力图（FG%）")

fig, ax = plt.subplots(figsize=(8, 7))

# 球场图（你已经上传了）
court = Image.open("court.png")
ax.imshow(court, extent=[-250, 250, 0, 470], alpha=0.6)

# ====== 关键：按“位置分箱 + FG%” ======
hb = ax.hexbin(
    df["loc_x"],
    df["loc_y"],
    C=df["shot_made_flag"],
    reduce_C_function=np.mean,   # ⭐变成命中率，不是数量
    gridsize=35,
    cmap="Reds",
    alpha=0.8,
    mincnt=1
)

cb = plt.colorbar(hb, ax=ax)
cb.set_label("FG%")

ax.set_title("Kobe Shot Heatmap")

# ❗去掉乱七八糟坐标（球场图必须这样）
ax.set_xticks([])
ax.set_yticks([])

st.pyplot(fig)