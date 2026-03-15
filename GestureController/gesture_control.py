import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import os
import socket
import pathlib

# ── Socket setup ────────────────────────────────────
sock       = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UNITY_IP   = "127.0.0.1"
UNITY_PORT = 5065

# ── Auto detect model path ───────────────────────────
SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
MODEL_PATH = str(SCRIPT_DIR / "hand_landmarker.task")

if not os.path.exists(MODEL_PATH):
    print("❌ Model file not found!")
    print(f"👉 Expected at: {MODEL_PATH}")
    exit()

print(f"✅ Model found at: {MODEL_PATH}")

# ── Setup Hand Detector ─────────────────────────────
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options      = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)
detector = vision.HandLandmarker.create_from_options(options)

# ── Webcam ──────────────────────────────────────────
cap = cv2.VideoCapture(1)

# ── Gesture State ───────────────────────────────────
last_gesture     = "open"
last_press_time  = 0
COOLDOWN         = 0.5
CONFIRM_FRAMES   = 3
fist_frame_count = 0
fps_start        = time.time()
fps_counter      = 0
fps_display      = 0

# ── Fist Detection ──────────────────────────────────
def is_fist(landmarks):
    tips     = [8, 12, 16, 20]
    knuckles = [6, 10, 14, 18]
    for tip, knuckle in zip(tips, knuckles):
        if landmarks[tip].y < landmarks[knuckle].y:
            return False
    return True

# ── Main Loop ───────────────────────────────────────
print("✅ Gesture control running in background!")
print("✊ FIST = Jump  |  ✋ OPEN PALM = Nothing")
print("🔌 Sending jumps to Unity on port 5065...")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame  = cv2.flip(frame, 1)
    rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_img)

    raw_fist = False

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            if is_fist(hand_landmarks):
                raw_fist = True

    if raw_fist:
        fist_frame_count += 1
    else:
        fist_frame_count = 0

    gesture = "fist" if fist_frame_count >= CONFIRM_FRAMES else "open"

    # ── Send JUMP to Unity ───────────────────────────
    now = time.time()
    if gesture == "fist" and last_gesture == "open":
        if now - last_press_time > COOLDOWN:
            sock.sendto(b"JUMP", (UNITY_IP, UNITY_PORT))
            last_press_time = now
            print("✊ JUMP sent to Unity!")

    last_gesture = gesture

    # FPS log in terminal
    fps_counter += 1
    if time.time() - fps_start >= 1.0:
        fps_display = fps_counter
        fps_counter = 0
        fps_start   = time.time()
        print(f"📷 FPS: {fps_display} | Gesture: {gesture}")

cap.release()
sock.close()
print("👋 Gesture control stopped.")