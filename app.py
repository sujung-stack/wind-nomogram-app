import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd

# 폰트 설정
try:
    font_path = "./NanumGothic.ttf"
    fontprop = fm.FontProperties(fname=font_path, size=12)
    plt.rcParams['font.family'] = fontprop.get_name()
except:
    plt.rcParams['font.family'] = 'sans-serif'

# 데이터 예시
data = {
    '지점': ['A-1', 'B-2', 'C-3', 'D-4'],
    'Lawson 등급': ['B', 'C', 'D', 'A'],
    'NEN8100 등급': ['B', 'B', 'D', 'A'],
    'Murakami 등급': [3, 3, 4, 1],
    '종합 평가': ['주의', '주의', '위험', '안전']
}
df = pd.DataFrame(data)

# Streamlit UI
st.title("📊 평가 결과 요약")
st.dataframe(df)
csv = df.to_csv(index=False).encode('utf-8-sig')
st.download_button("📥 결과 CSV 다운로드", csv, "evaluation_result.csv", "text/csv")

st.markdown("### 🧭 노모그램 시각화")

# 등급 정의
levels = ['A', 'B', 'C', 'D', 'E']
colors_nen = ['#0000FF', '#00BFFF', '#00FFFF', '#7CFC00', '#FF0000']
colors_lawson = ['#0000FF', '#00BFFF', '#7CFC00', '#FFFF00', '#FFA500', '#FF4500', '#FF0000']
colors_murakami = ['#0000FF', '#00BFFF', '#00FFFF', '#7CFC00', '#FF0000']

# 축 설정
fig, ax = plt.subplots(figsize=(8, 10))
ax.set_xlim(0, 3)
ax.set_ylim(0, 1)
ax.axis('off')

axes_x = [0, 1.5, 3]
axes_titles = ['NEN8100 (%)', 'Lawson 2001 (m/s)', 'Murakami (V/V∞)']
colors_dict = {
    'NEN8100': colors_nen,
    'Lawson': colors_lawson[-5:],  # 길이 맞추기
    'Murakami': colors_murakami
}

# 축별 색상 막대
for i, (x, title) in enumerate(zip(axes_x, axes_titles)):
    for j, level in enumerate(levels[::-1]):
        rect = patches.Rectangle((x - 0.08, j * 0.2), 0.16, 0.2, facecolor=colors_dict[title.split()[0]][j], edgecolor='white')
        ax.add_patch(rect)
    ax.text(x, 1.03, title, ha='center', va='bottom', fontsize=16, fontweight='bold')

# 지점 점선 및 라벨
for idx, row in df.iterrows():
    try:
        nen_idx = levels.index(row['NEN8100 등급'])
        lawson_idx = levels.index(row['Lawson 등급'])
        murakami_idx = 5 - int(row['Murakami 등급'])

        y_nen = nen_idx * 0.2 + 0.1
        y_lawson = lawson_idx * 0.2 + 0.1
        y_mura = murakami_idx * 0.2 + 0.1

        ax.plot([axes_x[0], axes_x[1]], [y_nen, y_lawson], linestyle='--', linewidth=2.5, color='gray')
        ax.plot([axes_x[1], axes_x[2]], [y_lawson, y_mura], linestyle='--', linewidth=2.5, color='gray')

        # 이름은 막대 옆으로 분리해서 출력
        ax.text(axes_x[2] + 0.1, y_mura, row['지점'], va='center', ha='left', fontsize=13, fontweight='bold')
    except:
        continue

st.pyplot(fig)
