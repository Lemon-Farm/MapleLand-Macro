import cv2
import numpy as np
import pyautogui as pag
import time
import random
import keyboard

main_image = cv2.imread("C:/Users/fnf00/Desktop/python/conda/result_01.png")

while True:
    # 이미지 로드
    screenshot = pag.screenshot(region=(82, 159, 137, 226))
    template = np.array(screenshot)
    template = cv2.cvtColor(template, cv2.COLOR_RGB2BGR)

    # 템플릿 매칭 수행
    result = cv2.matchTemplate(main_image, template, cv2.TM_CCOEFF_NORMED)

    # 최대 일치도의 위치 찾기
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 템플릿의 위치 및 크기
    top_left = max_loc
    w, h = template.shape[1], template.shape[0]
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # 매칭된 영역만 잘라내기
    cropped_image = main_image[
        top_left[1]: bottom_right[1], top_left[0]: bottom_right[0]
    ]

    # 이미지 로드
    image1 = template
    image2 = cropped_image

    # 첫 번째 이미지에서 (255, 255, 0) 색상 픽셀 좌표 찾기
    positions1 = np.where(np.all(image1 == [136, 255, 255], axis=-1))
    if len(positions1[0]) > 0:
        y1 = min(positions1[0])
    else:
        y1 = None

    # 두 번째 이미지에서 (0, 0, 255) 색상 픽셀 좌표 찾기 (아래에서부터, 첫 번째 색상 픽셀 높이 이상)
    positions2 = np.where(np.all(image2 == [255, 0, 255], axis=-1))
    if y1 is not None and len(positions2[0]) > 0:
        valid_indices = np.where(positions2[0] <= y1 - 3)[0]
        if len(valid_indices) > 0:
            idx = valid_indices[-1]  # 가장 아래쪽(오른쪽) 픽셀 선택
            coord2 = (positions2[1][idx], positions2[0][idx])
        else:
            coord2 = None
    else:
        coord2 = None
    # cv2.circle(image2, (positions1[1][0], y1), 0, (255, 0, 255), -1)
    # cv2.imwrite("result.png", image2)
    # cv2.circle(image2, (positions2[0], positions2[1]), 5, (255, 0, 0), -1)
    # 좌표 차이 계산 및 출력
    delta_x = coord2[0] - positions1[1][0]
    delta_y = coord2[1] - y1

    if delta_x > 0:
        if delta_x > 2:
            keyboard.release("left")
            keyboard.press("right")
        else:
            keyboard.press("right")
            time.sleep(random.uniform(0.04, 0.06))
            keyboard.release("right")
            time.sleep(random.uniform(0.09, 0.1))
    elif delta_x < 0:
        if delta_x < -2:
            keyboard.release("right")
            keyboard.press("left")
        else:
            keyboard.press("left")
            time.sleep(random.uniform(0.04, 0.06))
            keyboard.release("left")
            time.sleep(random.uniform(0.09, 0.1))
    else:
        keyboard.release("right")
        keyboard.release("left")
        if delta_y <= -3:
            pag.keyDown("up")
            if delta_y < -13:
                pag.press("f")
            else:
                pag.press("d")
