import cv2
import numpy as np
import pyautogui
import time

# ---------------------------
# CONFIG
# ---------------------------
THRESHOLD = 0.7
MOVE_DELAY = 0.15
COLLISION_DISTANCE = 50  # ระยะถือว่าชนศัตรูแล้ว

# ---------------------------
# LOAD ENEMY TEMPLATES
# ---------------------------
enemy_templates = [
    cv2.imread("enemy_left.png", cv2.IMREAD_GRAYSCALE),
    cv2.imread("enemy_right.png", cv2.IMREAD_GRAYSCALE),
    cv2.imread("enemy_up.png", cv2.IMREAD_GRAYSCALE),
    cv2.imread("enemy_down.png", cv2.IMREAD_GRAYSCALE),
]

# ---------------------------
# FIND ENEMY
# ---------------------------
def find_enemy(gray_frame, templates):
    best_val = 0
    best_loc = None
    best_template = None

    for template in templates:
        result = cv2.matchTemplate(
            gray_frame, template, cv2.TM_CCOEFF_NORMED
        )
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > best_val:
            best_val = max_val
            best_loc = max_loc
            best_template = template

    return best_val, best_loc, best_template

# ---------------------------
# STOP MOVEMENT
# ---------------------------
def stop_all_keys():
    for key in ["w", "a", "s", "d"]:
        pyautogui.keyUp(key)

# ---------------------------
# MAIN LOOP
# ---------------------------
print("🤖 Bot started...")
time.sleep(2)

while True:
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    score, loc, template = find_enemy(gray, enemy_templates)

    if score >= THRESHOLD:
        h, w = template.shape
        enemy_x = loc[0] + w // 2
        enemy_y = loc[1] + h // 2

        screen_h, screen_w = gray.shape
        center_x = screen_w // 2
        center_y = screen_h // 2

        dx = enemy_x - center_x
        dy = enemy_y - center_y

        # 🔴 CHECK COLLISION
        if abs(dx) < COLLISION_DISTANCE and abs(dy) < COLLISION_DISTANCE:
            stop_all_keys()
            print("⚔️ ชนศัตรูแล้ว → โจมตี")
            time.sleep(0.3)
            continue

        # 🟢 MOVE TOWARD ENEMY
        if abs(dx) > abs(dy):
            if dx > 0:
                pyautogui.keyDown("d")
                time.sleep(MOVE_DELAY)
                pyautogui.keyUp("d")
            else:
                pyautogui.keyDown("a")
                time.sleep(MOVE_DELAY)
                pyautogui.keyUp("a")
        else:
            if dy > 0:
                pyautogui.keyDown("s")
                time.sleep(MOVE_DELAY)
                pyautogui.keyUp("s")
            else:
                pyautogui.keyDown("w")
                time.sleep(MOVE_DELAY)
                pyautogui.keyUp("w")

    else:
        stop_all_keys()
        print("❌ ไม่เจอศัตรู")

    time.sleep(0.1)
