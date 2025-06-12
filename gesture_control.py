# gesture_utils.py

import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

prev_x, prev_y = 0, 0
gesture_cooldown = 1.0  # Cooldown in seconds
last_gesture_time = 0

def detect_gesture(frame):
    global prev_x, prev_y, last_gesture_time

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    h, w, _ = frame.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get index fingertip (landmark 8)
            cx = int(hand_landmarks.landmark[8].x * w)
            cy = int(hand_landmarks.landmark[8].y * h)

            # Draw circle on fingertip
            cv2.circle(frame, (cx, cy), 10, (255, 0, 255), -1)

            dx = cx - prev_x
            dy = cy - prev_y

            current_time = time.time()

            if current_time - last_gesture_time > gesture_cooldown:
                if abs(dx) > 60:
                    if dx > 0:
                        pyautogui.press("right")
                        print("👉 Swipe Right")
                        cv2.putText(frame, "👉 Swipe Right", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                    else:
                        pyautogui.press("left")
                        print("👈 Swipe Left")
                        cv2.putText(frame, "👈 Swipe Left", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                    last_gesture_time = current_time

                elif abs(dy) > 60:
                    if dy > 0:
                        pyautogui.press("down")
                        print("👇 Swipe Down")
                        cv2.putText(frame, "👇 Swipe Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                    else:
                        pyautogui.press("up")
                        print("👆 Swipe Up")
                        cv2.putText(frame, "👆 Swipe Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                    last_gesture_time = current_time

            prev_x, prev_y = cx, cy

    return frame
