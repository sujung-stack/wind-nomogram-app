import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import numpy as np

# 한글 폰트 설정 (환경에 맞게 조정 필요)
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()

# 앱 제목
st.title("📊 평가 결과 요약")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 등급 분류 함수
    def classify_nen(p):  # 초과확률
        if p < 2.5: return 'A'
        elif p < 5: return 'B'
        elif p < 10: return 'C'
        elif p < 20: return 'D'
        else: return 'E'

    def classify_lawson(v):  # 풍속
        if v < 2: return 'A'
        elif v < 4: return 'B'
        elif v < 6: return 'C'
        elif v < 8: return 'D'
        elif v < 10: return 'E'
        elif v < 15: return 'S1'
        else: return 'S2'

    def classify_murakami(vv):  # 풍속비
        if vv < 1.1: return 1
        elif vv < 1.3: return 2
        elif vv < 1.5: return 3
        else: return 4

    # 등급 계산
    df['Lawson 등급'] = df['풍속'].apply(classify_lawson)
    df['NEN8100 등급'] = df['초과확률'].apply(classify_nen)
    df['Murakami 등급'] = df['풍속비'].apply(classify_murakami)

    # 종합 평가
    def evaluate(row):
        if row['Murakami 등급'] >= 4 or row['NEN8100 등급'] == 'E':
            return '위험'
        elif row['Murakami 등급'] == 3:
            return '주의'
        else:
            return '안전'

    df['종합 평가'] = df.apply(evaluate, axis=1)

    st.dataframe(df[['지점', 'Lawson 등급', 'NEN8100 등급', 'Murakami 등급', '종합 평가']])
    st.download_button("📥 결과 CSV 다운로드", data=df.to_csv(index=False).encode('utf-8-sig'),
                       file_name="wind_eval_result.csv", mime='text/csv')

    # 노모그램 시각화
    st.markdown("## 🧭 노모그램 시각화")

    fig, ax = plt.subplots(figsize=(10, 6))
    levels = [
        ['A', 'B', 'C', 'D', 'E'],       # NEN8100
        ['A', 'B', 'C', 'D', 'E', 'S1', 'S2'],  # Lawson
        [1, 2, 3, 4]                     # Murakami
    ]
    colors = ['blue', 'dodgerblue', 'cyan', 'limegreen', 'red', 'orange', 'brown']
    pos = [0, 1, 2]

    # 막대 시각화
    for i in range(3):
        for j, lvl in enumerate(levels[i]):
            y = j / len(levels[i])
            h = 1 / len(levels[i])
            ax.add_patch(patches.Rectangle((pos[i] - 0.3, y), 0.6, h,
                                           color=colors[j % len(colors)], ec='black'))

    # 지점별 점선 + 레이블 표시
    for idx, row in df.iterrows():
        try:
            nen_idx = levels[0].index(row['NEN8100 등급']) + 0.5
            lawson_idx = levels[1].index(row['Lawson 등급']) + 0.5
            murakami_idx = levels[2].index(row['Murakami 등급']) + 0.5
            y_nen = nen_idx / len(levels[0])
            y_law = lawson_idx / len(levels[1])
            y_mur = murakami_idx / len(levels[2])

            ax.plot([0, 1, 2], [y_nen, y_law, y_mur],
                    linestyle='--', color='gray', linewidth=1.0)
            ax.text(2.35, y_mur, row['지점'], fontsize=10, va='center', fontproperties=fontprop)
        except Exception as e:
            st.warning(f"{row['지점']} 처리 중 오류 발생: {e}")
            continue

    ax.set_xlim(-0.5, 2.8)
    ax.set_ylim(0, 1)
    ax.set_xticks(pos)
    ax.set_xticklabels(['NEN8100 (%)', 'Lawson 2001 (m/s)', 'Murakami (V/V′)'])
    ax.set_ylabel("Normalization 0–1")
    ax.set_title("Nomogram", fontsize=14, fontproperties=fontprop)
    st.pyplot(fig)
