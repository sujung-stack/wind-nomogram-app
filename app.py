import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import numpy as np
import os

# 페이지 설정
st.set_page_config(page_title="풍환경 종합 안전평가", layout="wide")

# 제목
st.title("📊 평가 결과 요약")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    # CSV 다운로드 버튼
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 결과 CSV 다운로드",
        data=csv,
        file_name='evaluation_result.csv',
        mime='text/csv',
    )

    st.markdown("## 🧭 노모그램 시각화")

    # 폰트 설정
    try:
        font_path = "NanumGothic.ttf"
        fontprop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = fontprop.get_name()
    except Exception as e:
        st.warning(f"폰트 로드 실패: {e}")
        plt.rcParams['font.family'] = 'sans-serif'

    # 색상 설정
    colors = {
        'A': '#0000FF',  # 파랑
        'B': '#3399FF',  # 하늘
        'C': '#00FFFF',  # 청록
        'D': '#7CFC00',  # 연두
        'E': '#FF0000',  # 빨강
    }

    murakami_colors = ['#0000FF', '#3399FF', '#00FFFF', '#7CFC00', '#FF0000']
    lawson_colors = ['#0000FF', '#3399FF', '#00FFFF', '#7CFC00', '#FFFF00', '#FFA500', '#FF0000']
    nen_colors = ['#0000FF', '#3399FF', '#00FFFF', '#7CFC00', '#FF0000']

    # 기준 등급 정의
    nen_levels = ['A', 'B', 'C', 'D', 'E']
    lawson_levels = ['A', 'B', 'C', 'D', 'E', 'S1', 'S2']
    murakami_levels = ['1', '2', '3', '4']

    # 시각화
    fig, ax = plt.subplots(figsize=(9, 8))

    # 막대 너비
    bar_width = 0.2

    # NEN8100
    for i, level in enumerate(nen_levels):
        ax.add_patch(patches.Rectangle((0, i / len(nen_levels)), bar_width, 1 / len(nen_levels), color=colors[level]))

    # Lawson
    for i in range(len(lawson_levels)):
        ax.add_patch(patches.Rectangle((0.4, i / len(lawson_levels)), bar_width, 1 / len(lawson_levels), color=lawson_colors[i]))

    # Murakami
    for i in range(len(murakami_levels)):
        ax.add_patch(patches.Rectangle((0.8, i / len(murakami_levels)), bar_width, 1 / len(murakami_levels), color=murakami_colors[i]))

    # 등급 기준 텍스트
    ax.text(0.05, 1.02, "NEN8100 (%)", fontsize=10)
    ax.text(0.45, 1.02, "Lawson 2001 (m/s)", fontsize=10)
    ax.text(0.85, 1.02, "Murakami (V/V∞)", fontsize=10)

    # 지점별 점선 그리기
    for idx, row in df.iterrows():
        try:
            nen_idx = nen_levels.index(row['NEN8100 등급'])
            lawson_idx = lawson_levels.index(row['Lawson 등급'])
            murakami_idx = murakami_levels.index(str(row['Murakami 등급']))

            # y 위치
            y_nen = (nen_idx + 0.5) / len(nen_levels)
            y_lawson = (lawson_idx + 0.5) / len(lawson_levels)
            y_murakami = (murakami_idx + 0.5) / len(murakami_levels)

            # 점선 연결
            ax.plot([0.1, 0.5, 0.9], [y_nen, y_lawson, y_murakami], linestyle='--', color='gray', linewidth=2)

            # 지점 이름은 막대 옆으로
            ax.text(0.93, y_murakami, row['지점'], fontsize=11, verticalalignment='center', fontproperties=fontprop)

        except Exception as e:
            st.error(f"{row['지점']} 시각화 오류: {e}")

    ax.set_xlim(0, 1.2)
    ax.set_ylim(0, 1.05)
    ax.axis('off')

    st.pyplot(fig)
