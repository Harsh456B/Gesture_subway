import cv2
import mediapipe as mp
import pyautogui

# MediaPipe Hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

prev_x, prev_y = 0, 0
gesture_threshold = 40  # Minimum distance to consider a gesture


def detect_gesture(frame):
    global prev_x, prev_y

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_tip = hand_landmarks.landmark[8]  # Index finger tip
            cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

            dx = cx - prev_x
            dy = cy - prev_y

            if abs(dx) > gesture_threshold or abs(dy) > gesture_threshold:
                if abs(dx) > abs(dy):
                    if dx > 0:
                        pyautogui.press('right')
                        print("Swipe Right")
                    else:
                        pyautogui.press('left')
                        print("Swipe Left")
                else:
                    if dy > 0:
                        pyautogui.press('down')
                        print("Swipe Down")
                    else:
                        pyautogui.press('up')
                        print("Swipe Up")

                prev_x, prev_y = cx, cy

    return frame
