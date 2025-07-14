import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 페이지 설정
st.set_page_config(page_title="풍환경 종합 안전평가 시스템", layout="wide")

# 제목
st.title("🌬️ 풍환경 종합 안전평가 시스템")
st.markdown("""
CSV 파일을 업로드하면, 각 지점별 **Lawson / NEN8100 / Murakami** 기준 등급과 종합 평가 결과를 확인할 수 있습니다.
""")

# CSV 업로드
uploaded_file = st.file_uploader("📤 평가용 CSV 파일 업로드 (지점, 풍속, 초과확률, 풍속비)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    required_cols = ['지점', '풍속', '초과확률', '풍속비']
    if not all(col in df.columns for col in required_cols):
        st.error("❌ CSV에 다음 열이 포함되어야 합니다: 지점, 풍속, 초과확률, 풍속비")
    else:
        # 평가 기준 함수
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
            if "E" in (law, nen) or law == "S2" or mura == "4":
                return "위험"
            elif "D" in (law, nen) or law == "S1" or mura == "3":
                return "주의"
            else:
                return "안전"

        # 등급 평가 적용
        df['Lawson 등급'] = df['풍속'].apply(lawson_grade)
        df['NEN8100 등급'] = df['초과확률'].apply(nen_grade)
        df['Murakami 등급'] = df['풍속비'].apply(murakami_grade)
        df['종합 평가'] = df.apply(lambda row: overall_eval(row['Lawson 등급'], row['NEN8100 등급'], row['Murakami 등급']), axis=1)

        # 평가 결과 표시
        st.subheader("📋 평가 결과 요약")
        st.dataframe(df[['지점', 'Lawson 등급', 'NEN8100 등급', 'Murakami 등급', '종합 평가']], use_container_width=True)

        # CSV 다운로드
        csv_result = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button("📥 평가 결과 CSV 다운로드", data=csv_result, file_name="wind_evaluation_result.csv", mime="text/csv")

        # 노모그램 시각화 (배경 + 점선 + 라벨)
        st.subheader("🧭 노모그램 시각화")

        # 등급 -> Y좌표 매핑
        grade_to_y = {
            "A": 0.1, "B": 0.25, "C": 0.4, "D": 0.6, "E": 0.8,
            "S1": 0.9, "S2": 1.0,
            "1": 0.1, "2": 0.3, "3": 0.6, "4": 0.85
        }

        # 배경 이미지 불러오기
        try:
            img = mpimg.imread("nomogram_background.png")
            fig, ax = plt.subplots(figsize=(5, 7))
            ax.imshow(img, extent=[0, 3, 0, 1])
            ax.set_xlim(0, 3)
            ax.set_ylim(0, 1)
            ax.axis("off")

            x_pos = [0.5, 1.5, 2.5]  # NEN, Lawson, Murakami 축 위치
            for idx, row in df.iterrows():
                try:
                    y_pos = [
                        grade_to_y[row['NEN8100 등급']],
                        grade_to_y[row['Lawson 등급']],
                        grade_to_y[row['Murakami 등급']]
                    ]
                    ax.plot(x_pos, y_pos, linestyle='--', color='gray', linewidth=1.5)
                    ax.text(x_pos[-1] + 0.05, y_pos[-1], row['지점'],
                            fontsize=9, va='center', color='black')
                except KeyError:
                    continue

            st.pyplot(fig)

        except FileNotFoundError:
            st.error("❌ 'nomogram_background.png' 파일이 앱 디렉토리에 없습니다. 이미지 파일을 확인해주세요.")
