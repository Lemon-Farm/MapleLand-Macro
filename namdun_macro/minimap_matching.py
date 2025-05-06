import cv2
import numpy as np
import pyautogui as pag

# 이미지 로드
screenshot = pag.screenshot(region=(82, 159, 137, 226))
template = np.array(screenshot)
template = cv2.cvtColor(template, cv2.COLOR_RGB2BGR)
main_image = cv2.imread("C:/Users/fnf00/Desktop/python/conda/result_01.png")

# 템플릿 매칭 수행
result = cv2.matchTemplate(main_image, template, cv2.TM_CCOEFF_NORMED)

# 최대 일치도의 위치 찾기
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# 템플릿의 위치 및 크기
top_left = max_loc
w, h = template.shape[1], template.shape[0]
bottom_right = (top_left[0] + w, top_left[1] + h)

# 대상 이미지에 사각형 그리기
cv2.rectangle(main_image, top_left, bottom_right, (0, 255, 0), 1)

# 결과 이미지 표시
cv2.imshow("Template Matched", main_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
