import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 등급 → y좌표
grade_to_y = {
    "A": 0.1, "B": 0.25, "C": 0.4, "D": 0.6, "E": 0.8,
    "S1": 0.9, "S2": 1.0,
    "1": 0.1, "2": 0.3, "3": 0.6, "4": 0.85
}

# 이미지 불러오기
img = mpimg.imread("nomogram_background.png")
fig, ax = plt.subplots(figsize=(6, 5.5))  # ✅ 비율 조정

# 이미지 표시
ax.imshow(img, extent=[-0.5, 2.5, 0, 1])  # ✅ 좌우 여백 포함

# 좌표 설정
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(0, 1)
ax.axis("off")

# 막대 중심 x좌표 (정확히 맞춤)
x_pos = [0, 1, 2]

# 선 및 지점 텍스트
for idx, row in df.iterrows():
    try:
        y_pos = [
            grade_to_y[row['NEN8100 등급']],
            grade_to_y[row['Lawson 등급']],
            grade_to_y[row['Murakami 등급']]
        ]
        ax.plot(x_pos, y_pos, linestyle='--', color='gray', linewidth=2)

        # ✅ y좌표 약간 위로 이동 (가독성 개선)
        ax.text(x_pos[-1] + 0.05, y_pos[-1] + 0.03, row['지점'],
                fontsize=10, va='center', color='black')

    except KeyError:
        continue

st.pyplot(fig)

