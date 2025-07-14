
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from PIL import Image

# 이미지 배경 로드
image_path = "final_nomogram_clean.png"
bg_image = Image.open(image_path)

# 폰트 설정
font_path = "NanumGothicBold.ttf"
fontprop = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = fontprop.get_name()

st.title("Nomogram 평가 시스템 (A안)")

# 사용자 입력값
st.sidebar.header("입력값 선택")
nen_val = st.sidebar.slider("NEN8100 정규화값", 0.0, 1.0, 0.72)
lawson_val = st.sidebar.slider("Lawson 정규화값", 0.0, 1.0, 0.67)
murakami_val = st.sidebar.slider("Murakami 정규화값", 0.0, 1.0, 0.62)

# Plotting
fig, ax = plt.subplots(figsize=(7, 9))
ax.imshow(bg_image)

# 연결선 위치 계산 (색상칩 x축 위치 기준)
x_pos = [174, 495, 823]  # 이미지상의 픽셀 위치에 맞게 수동 조정 필요
y_pixels = np.array([nen_val, lawson_val, murakami_val])
y_pixels = (1 - y_pixels) * bg_image.size[1]  # 상단 기준

# 연결선 그리기
ax.plot(x_pos, y_pixels, color='black', linewidth=3)

# 축 제거
ax.axis('off')

st.pyplot(fig)
