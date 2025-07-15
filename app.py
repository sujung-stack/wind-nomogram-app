import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.font_manager as fm
import numpy as np
import os

# 사용자 지정 폰트 설정
FONT_PATH = "NanumGothicBold.ttf"
font_prop = fm.FontProperties(fname=FONT_PATH, size=12)

# 배경 이미지 경로
BG_IMAGE_PATH = "nomogram_base.png"

# 정규화 함수 정의 (0~1)
def normalize(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val)

# 기준별 정규화 범위
ranges = {
    "NEN8100": [0, 25],         # 초과확률 %
    "Lawson": [0, 20],          # 풍속 m/s
    "Murakami": [0.0, 2.0],     # 풍속비
}

st.set_page_config(layout="centered")
st.title("🌀 풍환경 종합 안전평가 시스템")
st.markdown("CSV 파일을 업로드하면 각 지점별 **Lawson / NEN8100 / Murakami 등급과 종합평가**를 수행하고 노모그램 위에 시각화합니다.")

uploaded_file = st.file_uploader("📂 CSV 파일 업로드 (예: 지점, 풍속, 초과확률, 풍속비)", type=["csv"])

# 샘플 데이터 보기
with st.expander("📄 예시 CSV 파일 보기"):
    st.write(pd.DataFrame({
        '지점': ['A-1', 'B-2', 'C-3', 'D-4'],
        '풍속': [6.2, 7.5, 9.8, 3.3],
        '초과확률': [4.2, 6.8, 12.1, 1.2],
        '풍속비': [1.1, 1.3, 1.6, 0.9]
    }))

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    required_cols = {'지점', '풍속', '초과확률', '풍속비'}

    if not required_cols.issubset(df.columns):
        st.error("❌ CSV에 다음 열이 포함되어야 합니다: 지점, 풍속, 초과확률, 풍속비")
    else:
        # 정규화 좌표 계산
        nen_norm = normalize(df['초과확률'], *ranges['NEN8100'])
        lawson_norm = normalize(df['풍속'], *ranges['Lawson'])
        murakami_norm = normalize(df['풍속비'], *ranges['Murakami'])

        df['NEN_norm'] = nen_norm
        df['Lawson_norm'] = lawson_norm
        df['Murakami_norm'] = murakami_norm

        # 평가 등급 추가 (간략화 예시)
        df['Lawson 등급'] = pd.cut(df['풍속'], bins=[0, 4, 6, 8, 10, 15, 20], labels=['A', 'B', 'C', 'D', 'E'], right=False)
        df['NEN8100 등급'] = pd.cut(df['초과확률'], bins=[0, 2.5, 5, 10, 20, 100], labels=['A', 'B', 'C', 'D', 'E'], right=False)
        df['Murakami 등급'] = pd.cut(df['풍속비'], bins=[0, 1.0, 1.1, 1.5, 2.0], labels=[1, 2, 3, 4], right=False)

        df['종합 평가'] = df[['Lawson 등급', 'NEN8100 등급', 'Murakami 등급']].apply(lambda row: '위험' if 'E' in row.values or '4' in row.values else '주의' if 'D' in row.values or '3' in row.values else '안전', axis=1)

        st.dataframe(df[['지점', '풍속', '초과확률', '풍속비', 'Lawson 등급', 'NEN8100 등급', 'Murakami 등급', '종합 평가']])

        # 📈 시각화
        st.markdown("### ⏱️ 노모그램 시각화")

        fig, ax = plt.subplots(figsize=(6.6, 10))
        bg_img = mpimg.imread(BG_IMAGE_PATH)
        ax.imshow(bg_img, extent=[0, 3, 0, 1])

        x_vals = [0.15, 1.5, 2.85]  # 축 위치

        for i, row in df.iterrows():
            y_vals = [row['NEN_norm'], row['Lawson_norm'], row['Murakami_norm']]
            ax.plot(x_vals, y_vals, linestyle='--', color='gray', linewidth=1)
            ax.text(x_vals[0]-0.05, y_vals[0], row['지점'], fontproperties=font_prop,
                    ha='right', va='center', fontsize=11, weight='bold')

        ax.axis('off')
        st.pyplot(fig)

        # 결과 다운로드
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 결과 CSV 다운로드", csv, file_name="evaluation_result.csv", mime='text/csv')
