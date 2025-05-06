from ultralytics import YOLO
import cv2
import numpy as np
import torch
import time
import pyautogui as pag
import random
import keyboard
import multiprocessing


# 설정 변수
model = YOLO(
    "C:/Users/fnf00/Desktop/python/conda/runs2/detect/train/weights/best.pt")  # 모델 설정
region = (
    8,
    8,
    1936,
    1056,
)  # 스크린샷 범위 / (8, 8, 1936, 1056) : 전체화면 / (0, -7, 1296, 759) : 창모드
heal_region = (259, 208)  # 스킬 범위 / 캐릭터 기준 x축으로, y축으로
claw_region = (320, 128)  # 매직클로 범위
right_or_left = "left"  # 커즈아이가 왼쪽 ? 오른쪽


# 화면 캡쳐 및 박스 정보로 변환
def capture_and_detect():
    global region
    frame = pag.screenshot(region=region)
    result = model(frame)
    boxes = result[0].boxes  # 결과의 [0]번째가 '사진'임
    return boxes


# 박스의 좌표 리스트를 구함
def getList(box):
    pos = torch.flatten(box.xyxy)
    return pos.tolist()


# 리스트를 x, y좌표로 변환
def list_to_xy(pos_list, is_rope):
    x = (pos_list[0] + pos_list[2]) / 2
    if is_rope:  # 로프는 밑부분 좌표를 반환해야 하기 때문
        y = pos_list[3]
    else:
        y = (pos_list[1] + pos_list[3]) / 2
    return (x, y)


# 오브젝트들의 x, y값을 구함
def getPos(boxes):
    Charapos = (0, 0)
    Lupanposes = []
    Kuzzposes = []
    C_before = 0.0
    for box in boxes:
        match box.cls.item():
            case 0.0:
                if box.conf.item() >= 0.5 and box.conf.item() > C_before:
                    Charapos = list_to_xy(getList(box), False)
                    C_before = box.conf.item()
            case 1.0:
                if box.conf.item() >= 0.46:
                    Lupanpos = list_to_xy(getList(box), False)
                    Lupanposes.append(Lupanpos)
            case 2.0:
                if box.conf.item() >= 0.46:
                    kuzzpos = list_to_xy(getList(box), False)
                    Kuzzposes.append(kuzzpos)

    return (Charapos, Lupanposes, Kuzzposes)


# 자동 이동
def automove(shared_value):
    main_image = cv2.imread(
        "C:/Users/fnf00/Desktop/python/conda/result_01.png")
    down = True

    while True:
        if shared_value.value == False:
            if down:
                randkey = random.choice(["right", "left"])
                keyboard.press(randkey)
                time.sleep(0.1)
                keyboard.press("f")
                time.sleep(0.3)
                keyboard.release("f")
                time.sleep(0.1)
                keyboard.release(randkey)
                if shared_value.value == False:
                    time.sleep(0.4)
                continue
            keyboard.release("right")
            keyboard.release("left")
            time.sleep(0.3)
            if shared_value.value == False:
                time.sleep(0.4)
            continue
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
        cv2.imshow("Template Matched", cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # 첫 번째 이미지에서 (255, 255, 0) 색상 픽셀 좌표 찾기
        positions1 = np.where(np.all(image1 == [136, 255, 255], axis=-1))
        y1 = min(positions1[0])

        # 두 번째 이미지에서 (0, 0, 255) 색상 픽셀 좌표 찾기 (아래에서부터, 첫 번째 색상 픽셀 높이 이상)
        if down:
            positions2 = np.where(np.all(image2 == [255, 0, 255], axis=-1))
            if y1 is not None and len(positions2[0]) > 0:
                valid_indices = np.where(positions2[0] >= y1 + 3)[0]
                if len(valid_indices) > 0:
                    idx = valid_indices[0]  # 가장 아래쪽(오른쪽) 픽셀 선택
                    coord2 = (positions2[1][idx], positions2[0][idx])
                else:
                    coord2 = None
            else:
                coord2 = None

        else:
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

        # 최상단 도착하면 아래로 내려감
        if coord2 is None:
            down = not down
            continue

        delta_x = coord2[0] - positions1[1][0]
        delta_y = coord2[1] - y1
        if shared_value.value == False:
            time.sleep(0.5)
            continue
        if down:
            delta_x -= 8
            pag.keyUp("up")
            keyboard.release("up")
            if delta_x > 3:
                keyboard.release("left")
                keyboard.press("right")
            elif delta_x < -3 and delta_x != -8:
                keyboard.release("right")
                keyboard.press("left")
            else:
                randkey = random.choice(["right", "left"])
                keyboard.release("right")
                keyboard.release("left")
                if shared_value.value == False:
                    time.sleep(0.5)
                    continue
                keyboard.press("down")
                time.sleep(0.3)
                keyboard.press(randkey)
                keyboard.press("f")
                time.sleep(0.1)
                keyboard.release("f")
                keyboard.release(randkey)
                time.sleep(0.1)
                keyboard.release("down")
                time.sleep(1.0)
            continue

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
            if delta_x < -3:
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
            if shared_value.value == False:
                time.sleep(0.5)
                continue
            if delta_y <= -3:
                pag.keyDown("up")
                if delta_y < -13:
                    pag.press("f")
                    time.sleep(0.5)
                else:
                    pag.press("d")
                    time.sleep(0.5)


# 캐릭터 주위에 해당 오브젝트(몬스터)가 있는지 확인
def is_exist(Cpos, Mposes, Kuzz):
    global heal_region
    global claw_region
    skill_region = heal_region
    if Kuzz:
        skill_region = claw_region

    x = Cpos[0]
    y = Cpos[1]

    dx = skill_region[0]
    dy = skill_region[1]

    x_region = (x - dx, x + dx)
    y_region = (y - dy + 35, y + dy)
    if Kuzz:
        y_region = (y - 50, y + 90)

    global right_or_left
    for Mpos in Mposes:
        if x_region[0] <= Mpos[0] and Mpos[0] <= x_region[1]:
            if y_region[0] <= Mpos[1] and Mpos[1] <= y_region[1]:
                if Kuzz:
                    if Cpos[0] < Mpos[0]:
                        right_or_left = "right"
                    else:
                        right_or_left = "left"
                return True
    return False


# 코드 실행
if __name__ == "__main__":
    keyboard.release("`")
    # 자동이동 프로세스 실행
    shared_value = multiprocessing.Value("b", False)
    automover = multiprocessing.Process(target=automove, args=(shared_value,))
    automover.start()

    while True:
        boxes = capture_and_detect()
        objpos = getPos(boxes)

        Cpos = objpos[0]
        Lposes = objpos[1]
        Kposes = objpos[2]

        # 1순위 : 루팡 공격 / 2순위 : 커즈아이 공격
        if is_exist(Cpos, Lposes, False):
            pag.press("a")
            shared_value.value = False
        elif is_exist(Cpos, Kposes, True):
            keyboard.press(right_or_left)
            if right_or_left == "right":
                keyboard.release("left")
            else:
                keyboard.release("right")
            time.sleep(0.07)
            pag.press("s")
            keyboard.release(right_or_left)
            shared_value.value = False
        else:
            shared_value.value = True

        time.sleep(random.uniform(0.15, 0.2))
