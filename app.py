import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = "NanumGothicBold.ttf"  # 배포 시 경로 유의
fontprop = fm.FontProperties(fname=font_path, size=10)
plt.rcParams['font.family'] = fontprop.get_name()

st.set_page_config(layout="wide")
st.title("🌬️ 풍환경 종합 안전평가 시스템")
st.caption("다중 기준 (Lawson, Murakami, NEN8100)을 통합한 시각화 기반 노모그램")

# CSV 업로드
uploaded_file = st.file_uploader("📂 평가결과 CSV 업로드", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 평가 결과 요약")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 결과 CSV 다운로드", csv, "evaluation_results.csv", "text/csv")

    st.subheader("📈 노모그램 시각화")

    # 평가 기준 축 정보
    categories = ['NEN8100 (%)', 'Lawson 2001 (m/s)', 'Murakami (V/Vꞌ)']
    levels = [
        ['A', 'B', 'C', 'D', 'E'],
        ['A', 'B', 'C', 'D', 'E', 'S1', 'S2'],
        ['1', '2', '3', '4']
    ]
    colors = [
        ['#0000FF', '#3399FF', '#66CCFF', '#7CFC00', '#FF0000'],
        ['#0000FF', '#3399FF', '#66CCFF', '#7CFC00', '#FFFF00', '#FFA500', '#FF0000'],
        ['#0000FF', '#3399FF', '#7CFC00', '#FF0000']
    ]

    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 0.1

    for i, (cat, lvls, cols) in enumerate(zip(categories, levels, colors)):
        x = i * 1.5
        for j, (lvl, color) in enumerate(zip(reversed(lvls), reversed(cols))):
            height = 1 / len(lvls)
            y = j * height
            ax.add_patch(patches.Rectangle((x - bar_width/2, y), bar_width, height, color=color))
        ax.text(x, 1.03, cat, ha='center', va='bottom', fontsize=10, fontweight='bold')

    for idx, row in df.iterrows():
        try:
            nen_idx = levels[0].index(row['NEN8100 등급'])
            lawson_idx = levels[1].index(row['Lawson 등급'])
            murakami_idx = levels[2].index(str(row['Murakami 등급']))
        except ValueError:
            continue

        nen_y = (len(levels[0]) - nen_idx - 0.5) / len(levels[0])
        lawson_y = (len(levels[1]) - lawson_idx - 0.5) / len(levels[1])
        murakami_y = (len(levels[2]) - murakami_idx - 0.5) / len(levels[2])

        x_vals = [0 * 1.5 + 0.1, 1 * 1.5, 2 * 1.5 - 0.1]
        y_vals = [nen_y, lawson_y, murakami_y]

        ax.plot(x_vals, y_vals, linestyle='--', linewidth=1.5, color='gray')
        ax.text(x_vals[-1] + 0.05, y_vals[-1], row['지점'], fontsize=10, fontweight='bold', va='center')

    ax.set_xlim(-0.5, 3)
    ax.set_ylim(0, 1)
    ax.axis('off')
    st.pyplot(fig)
