import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import pandas as pd
import streamlit as st
import os

# 한글 폰트 설정 (NanumGothic이 존재할 경우)
font_path = "/mnt/data/NanumGothicBold.ttf"
if os.path.exists(font_path):
    fontprop = fm.FontProperties(fname=font_path, size=12)
    plt.rcParams['font.family'] = fontprop.get_name()
else:
    plt.rcParams['font.family'] = 'DejaVu Sans'

# 앱 제목
st.title("📊 평가 결과 요약")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
    st.download_button("📥 결과 CSV 다운로드", data=uploaded_file, file_name="result.csv")

    st.subheader("🧭 노모그램 시각화")

    # 기준 등급 정의
    levels = {
        'Lawson 등급': ['A', 'B', 'C', 'D', 'E'],
        'NEN8100 등급': ['A', 'B', 'C', 'D', 'E'],
        'Murakami 등급': [1, 2, 3, 4, 5]
    }

    # 색상 정의
    colors = ['#0000FF', '#00BFFF', '#00FFFF', '#7CFC00', '#FF0000']  # Blue → Red

    fig, ax = plt.subplots(figsize=(8, 10))
    bar_width = 0.5

    # 기준별 컬럼 생성
    for i, (label, grade_list) in enumerate(levels.items()):
        for j, grade in enumerate(grade_list):
            ax.add_patch(patches.Rectangle((i - bar_width / 2, j / 5), bar_width, 0.2, color=colors[j]))
        ax.text(i, 1.05, label, ha='center', fontsize=15, weight='bold')

    # 지점별 라인 및 레이블
    for _, row in df.iterrows():
        try:
            nen_idx = levels['NEN8100 등급'].index(row['NEN8100 등급'])
            lawson_idx = levels['Lawson 등급'].index(row['Lawson 등급'])
            murakami_idx = levels['Murakami 등급'].index(int(row['Murakami 등급']))
        except Exception:
            continue

        y_pts = [nen_idx / 5 + 0.1, lawson_idx / 5 + 0.1, murakami_idx / 5 + 0.1]
        ax.plot([0, 1, 2], y_pts, linestyle='--', linewidth=2, color='gray')

        # 마지막 막대 오른쪽에 텍스트
        ax.text(2.2, y_pts[2], row['지점'], fontsize=11, va='center', weight='bold')

    ax.set_xlim(-0.5, 2.8)
    ax.set_ylim(0, 1.1)
    ax.axis('off')
    st.pyplot(fig, use_container_width=False)
