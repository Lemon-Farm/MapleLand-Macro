import pygetwindow as gw

# 특정 창의 타이틀로 창을 찾습니다. 이는 창의 타이틀이 정확히 일치해야 합니다.
# 예를 들어, 웹 브라우저의 경우 탭의 제목이 될 수 있습니다.
window = gw.getWindowsWithTitle("MapleStory Worlds-Mapleland")[0]

# 창의 위치와 크기를 얻습니다.
top = window.top
left = window.left
width = window.width
height = window.height

print(top, left, width, height, sep=", ")
