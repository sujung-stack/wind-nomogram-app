
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 배경 이미지 로드
img = mpimg.imread("nomogram_background.png")
fig, ax = plt.subplots(figsize=(5, 7))

# 배경 노모그램 이미지 표시
ax.imshow(img, extent=[0, 3, 0, 1])  # x=[NEN, Lawson, Murakami], y=[0~1]

# 좌표 설정
ax.set_xlim(0, 3)
ax.set_ylim(0, 1)
ax.axis("off")

# 등급 → y좌표 매핑
grade_to_y = {
    "A": 0.1, "B": 0.25, "C": 0.4, "D": 0.6, "E": 0.8,
    "S1": 0.9, "S2": 1.0,
    "1": 0.1, "2": 0.3, "3": 0.6, "4": 0.85
}

# 꺾은선 위치: NEN → Lawson → Murakami 기준
x_pos = [0.5, 1.5, 2.5]

# 평가된 df 기준으로 점선 + 지점명 표시
for idx, row in df.iterrows():
    try:
        y_pos = [
            grade_to_y[row['NEN8100 등급']],
            grade_to_y[row['Lawson 등급']],
            grade_to_y[row['Murakami 등급']]
        ]
