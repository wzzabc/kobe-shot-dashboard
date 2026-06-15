import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import seaborn as sns

# =========================
# 页面配置
# =========================
st.set_page_config(page_title="Kobe Shot Dashboard", layout="wide")

# =========================
# ⭐ 解决中文显示问题（关键）
# =========================
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体
plt.rcParams['axes.unicode_minus'] = False

# =========================
# 数据读取
# =========================
df = pd.read_csv("data_cleaned.csv")

st.title("🏀 Kobe Bryant 投篮数据分析")

col1, col2 = st.columns(2)

# =========================
# 1. 投篮分布
# =========================
with col1:
    st.subheader("投篮分布")

    fig, ax = plt.subplots(figsize=(6,6))
    ax.scatter(df["loc_x"], df["loc_y"], s=1, alpha=0.5)

    ax.set_title("Shot Distribution")
    ax.set_xlabel("Court X")
    ax.set_ylabel("Court Y")

    # 字体不旋转（避免中文乱码）
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

    plt.xticks(rotation=0)  # ⭐ 中文不旋转
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

plt.xticks(rotation=0)  # ⭐ 修复中文倾斜问题
ax.set_ylim(0, 1)

ax.set_title("Distance FG%")

st.pyplot(fig)

# =========================
# 4. 🏀 球场热力图（升级版）
# =========================
st.subheader("🏀 投篮热力图（Shot Heatmap）")

fig, ax = plt.subplots(figsize=(8,7))

# 球场背景（你已经上传 court.png）
try:
    court = Image.open("court.png")
    ax.imshow(court, extent=[-250, 250, 0, 470], alpha=0.6)
except:
    st.warning("未找到 court.png")

# ⭐ 更合理热力图（KDE，比 hexbin 更像NBA分析）
sns.kdeplot(
    x=df["loc_x"],
    y=df["loc_y"],
    fill=True,
    cmap="Reds",
    alpha=0.5,
    ax=ax
)

ax.set_xlim(-250, 250)
ax.set_ylim(0, 470)

# 去掉坐标轴（更像专业NBA图）
ax.set_xticks([])
ax.set_yticks([])

ax.set_title("Kobe Shot Heatmap (FG Density)")

st.pyplot(fig)