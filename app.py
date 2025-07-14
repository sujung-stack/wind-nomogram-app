import streamlit as st
import pandas as pd
from PIL import Image

# 페이지 설정
st.set_page_config(page_title="풍환경 종합 안전평가 시스템", layout="wide")

# 제목
st.title("🌬️ 풍환경 종합 안전평가 시스템")
st.markdown("""
CSV 파일을 업로드하면, 각 지점별 **Lawson / NEN8100 / Murakami** 기준 등급,
그리고 종합 안전성 평가를 자동으로 수행하고, 노모그램으로 시각화합니다.
""")

# 샘플 CSV 안내
st.file_uploader("📤 CSV 파일 업로드 (예: data.csv)", type=["csv"], key="csv_upload", help="지점, 풍속(m/s), 초과확률(%), 풍속비 순")

# 예시용 링크 제공
with st.expander("📎 예시 CSV 파일 보기"):
    st.markdown("**형식:** `지점, 풍속, 초과확률, 풍속비`")
    st.code("A-1, 5.2, 3.1, 1.1\nB-2, 7.5, 4.8, 1.3")

# CSV 업로드
uploaded_file = st.file_uploader("👉 평가용 CSV 파일을 선택하세요", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 유효성 검사
    required_cols = ['지점', '풍속', '초과확률', '풍속비']
    if not all(col in df.columns for col in required_cols):
        st.error("❌ CSV에 다음 열이 포함되어야 합니다: 지점, 풍속, 초과확률, 풍속비")
    else:
        # 등급 평가 함수
        def lawson_grade(v):
            if v < 4: return "A"
            elif v < 6: return "B"
            elif v < 8: return "C"
            elif v < 10: return "D"
            elif v < 15: return "E"
            elif v < 20: return "S1"
            else: return "S2"

        def nen_grade(p):
            if p < 2.5: return "A"
            elif p < 5: return "B"
            elif p < 10: return "C"
            elif p < 20: return "D"
            else: return "E"

        def murakami_grade(r):
            if r < 1.0: return "1"
            elif r < 1.1: return "2"
            elif r < 1.5: return "3"
            else: return "4"

        def overall_eval(law, nen, mura):
            # 간단 예시 로직
            danger_set = {"E", "S2", "4"}
            if law in danger_set or nen in danger_set or mura in danger_set:
                return "위험"
            caution_set = {"D", "S1", "3"}
            if law in caution_set or nen in caution_set or mura in caution_set:
                return "주의"
            return "안전"

        # 등급 평가
        df['Lawson 등급'] = df['풍속'].apply(lawson_grade)
        df['NEN8100 등급'] = df['초과확률'].apply(nen_grade)
        df['Murakami 등급'] = df['풍속비'].apply(murakami_grade)
        df['종합 평가'] = df.apply(lambda row: overall_eval(row['Lawson 등급'], row['NEN8100 등급'], row['Murakami 등급']), axis=1)

        # 결과 표시
        st.subheader("📋 평가 결과 요약")
        st.dataframe(df[['지점', 'Lawson 등급', 'NEN8100 등급', 'Murakami 등급', '종합 평가']], use_container_width=True)

        # CSV 다운로드
        result_csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 결과 CSV 다운로드", data=result_csv, file_name="풍환경_평가결과.csv", mime="text/csv")

        # 노모그램 이미지 표시
        st.subheader("🧭 노모그램 시각화")
        st.image("final_nomogram_clean.png", caption="Lawson / NEN8100 / Murakami 기준 등급 비교표", use_column_width=True)
