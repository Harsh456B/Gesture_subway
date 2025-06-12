# app.py

import streamlit as st
import cv2
import webbrowser
from gesture_utils import detect_gesture

st.set_page_config(page_title="Gesture-Controlled Subway Surfers")

st.title("🖐️ Gesture-Controlled Subway Surfers")

# Manage webcam state
if "run_cam" not in st.session_state:
    st.session_state.run_cam = False

# Launch game
if st.button("🎮 Launch Game + Start Webcam"):
    webbrowser.open("https://poki.com/en/g/subway-surfers")
    st.session_state.run_cam = True

# Stop webcam
if st.session_state.run_cam:
    if st.button("⛔ Stop Webcam"):
        st.session_state.run_cam = False

# Show webcam
if st.session_state.run_cam:
    FRAME_WINDOW = st.image([])
    cap = cv2.VideoCapture(0)

    st.success("🟢 Webcam started. Use hand gestures to control the game.")

    while st.session_state.run_cam:
        ret, frame = cap.read()
        if not ret:
            st.error("❌ Could not access webcam.")
            break

        frame = detect_gesture(frame)
        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    cap.release()
    cv2.destroyAllWindows()
