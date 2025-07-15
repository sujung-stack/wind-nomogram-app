import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import io

# 나눔고딕 폰트 설정
font_path = "NanumGothic.ttf"  # 같은 폴더 내에 TTF 파일 필요
fontprop = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = fontprop.get_name()

# 색상 정의
colors_nen = ['#0000FF', '#4169E1', '#00FFFF', '#ADFF2F', '#FF0000']  # A-E
colors_lawson = ['#0000FF', '#00FFFF', '#FFFF00', '#FFA500', '#FF0000']
colors_murakami = ['#0000FF', '#1E90FF', '#00FFFF', '#ADFF2F', '#FF0000']

# 등급 매핑
nen_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
lawson_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
murakami_mapping = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}

# 페이지 설정
st.set_page_config(layout="centered")
st.title("📊 보행자 풍환경 평가 시스템")

# CSV 파일 업로드
uploaded_file = st.file_uploader("📂 CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 평가 결과 요약")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("💾 결과 CSV 다운로드", csv, "평가결과.csv", "text/csv")

    st.subheader("🧭 노모그램 시각화")
    fig, ax = plt.subplots(figsize=(8, 8))

    # 색상 막대
    for i, color in enumerate(colors_nen):
        ax.add_patch(patches.Rectangle((0, i*0.2), 0.2, 0.2, color=color))
    for i, color in enumerate(colors_lawson):
        ax.add_patch(patches.Rectangle((0.4, i*0.2), 0.2, 0.2, color=color))
    for i, color in enumerate(colors_murakami):
        ax.add_patch(patches.Rectangle((0.8, i*0.2), 0.2, 0.2, color=color))

    # 지점별 라벨 및 연결선
    for idx, row in df.iterrows():
        name = row['지점']
        nen = nen_mapping.get(row['NEN8100 등급'], 2)
        lawson = lawson_mapping.get(row['Lawson 등급'], 2)
        murakami = murakami_mapping.get(int(row['Murakami 등급']), 2)

        x = [0.2, 0.4, 0.8]
        y = [1 - (nen+0.5)*0.2, 1 - (lawson+0.5)*0.2, 1 - (murakami+0.5)*0.2]

        ax.plot(x, y, 'k--', linewidth=1.2, alpha=0.6)
        ax.text(0.82, y[2], name, fontsize=11, fontproperties=fontprop, verticalalignment='center')

    # 축 제거 및 제목
    ax.axis('off')
    ax.set_xlim(0, 1.1)
    ax.set_ylim(0, 1)

    ax.text(0.1, 1.05, "NEN8100 (%)", ha="center", fontsize=14, fontproperties=fontprop)
    ax.text(0.5, 1.05, "Lawson 2001 (m/s)", ha="center", fontsize=14, fontproperties=fontprop)
    ax.text(0.9, 1.05, "Murakami (V/V∞)", ha="center", fontsize=14, fontproperties=fontprop)

    st.pyplot(fig)
else:
    st.info("CSV 파일을 먼저 업로드해주세요.")
