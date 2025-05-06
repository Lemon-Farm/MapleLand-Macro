from pynput.mouse import Listener

print(1013 - 741, 597 - 459)


def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y})")


# 마우스 이벤트 리스너 시작
with Listener(on_click=on_click) as listener:
    listener.join()
