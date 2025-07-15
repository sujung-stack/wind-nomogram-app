import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

# 사용자 업로드 CSV 샘플 예시
EXAMPLE_CSV = """지점,풍속,초과확률,풍속비
A-1,6,0.03,1.0
B-2,8,0.01,1.3
C-3,12,0.05,1.6
D-4,3,0.002,0.8
"""

# 평가 함수
def 평가등급(풍속, 초과확률, 풍속비):
    # Lawson
    if 초과확률 > 0.023 and 풍속 >= 15:
        lawson = "S2"
    elif 초과확률 > 0.023 and 풍속 >= 10:
        lawson = "S1"
    elif 초과확률 > 0.05:
        lawson = "E"
    elif 풍속 >= 10:
        lawson = "D"
    elif 풍속 >= 8:
        lawson = "C"
    elif 풍속 >= 6:
        lawson = "B"
    else:
        lawson = "A"

    # NEN8100
    if 초과확률 >= 0.20:
        nen = "E"
    elif 초과확률 >= 0.10:
        nen = "D"
    elif 초과확률 >= 0.05:
        nen = "C"
    elif 초과확률 >= 0.025:
        nen = "B"
    else:
        nen = "A"

    # Murakami
    if 풍속비 > 1.5:
        murakami = 4
    elif 풍속비 > 1.1:
        murakami = 3
    elif 풍속비 > 1.0:
        murakami = 2
    else:
        murakami = 1

    # 통합 평가 (간단히 예시)
    if "S2" in lawson or nen == "E" or murakami == 4:
        result = "위험"
    elif lawson in ["D", "E"] or nen in ["D"] or murakami >= 3:
        result = "주의"
    else:
        result = "안전"

    return lawson, nen, murakami, result


# 📌 Streamlit UI
st.set_page_config(page_title="풍환경 노모그램 평가 시스템", layout="centered")

st.markdown("## 🌬️ 풍환경 종합 안전평가 시스템")
st.write("CSV 파일을 업로드하면 각 지점별 **Lawson / NEN8100 / Murakami 등급**과 **종합평가**를 수행하고 노모그램 위에 시각화합니다.")

uploaded_file = st.file_uploader("📄 CSV 파일 업로드 (예: 지점, 풍속, 초과확률, 풍속비)", type=["csv"])

if st.button("📁 예시 CSV 파일 보기"):
    st.code(EXAMPLE_CSV, language="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    필수열 = {"지점", "풍속", "초과확률", "풍속비"}
    if not 필수열.issubset(df.columns):
        st.error(f"CSV에 다음 열이 포함되어야 합니다: {', '.join(필수열)}")
    else:
        # 등급 산정
        df[["Lawson 등급", "NEN8100 등급", "Murakami 등급", "종합 평가"]] = df.apply(
            lambda row: pd.Series(평가등급(row["풍속"], row["초과확률"], row["풍속비"])), axis=1
        )
        st.dataframe(df)

        # 📤 CSV 다운로드
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 결과 CSV 다운로드", data=csv, file_name="평가결과.csv", mime="text/csv")

        st.markdown("### 🧭 노모그램 시각화")

        # 배경 이미지 불러오기
        bg_img = Image.open("nomogram_background.png").convert("RGBA")
        draw = ImageDraw.Draw(bg_img)

        # 폰트 설정 (업로드한 NanumGothic)
        font_path = "NanumGothicBold.ttf"
        font = ImageFont.truetype(font_path, 40)

        # 위치 매핑 함수 (예시 값 기준)
        def normalize(value, min_val, max_val):
            return 1.0 - (value - min_val) / (max_val - min_val)

        for idx, row in df.iterrows():
            y = 100 + normalize(row["초과확률"], 0.0, 0.25) * 800  # y 좌표 (예시)
            x = {"NEN8100": 90, "Lawson": 310, "Murakami": 530}
            color = (0, 0, 0, 255)

            for label, xpos in x.items():
                draw.text((xpos, y), row["지점"], fill=color, font=font)

        # 결과 표시
        st.image(bg_img, caption="노모그램 시각화", use_column_width=True)
