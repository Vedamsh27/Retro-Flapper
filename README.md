# 🐦 Retro Flapper — The Angry Bird Edition

> A Flappy Bird clone built in Unity, upgraded with **AI-powered hand gesture control** using computer vision.

![Demo](demo/demo.gif)

---

## ✨ What is this?

Retro Flapper started as a classic Flappy Bird clone — our beloved Angry Bird navigating through endless pipe obstacles. It was then upgraded into an **AI + Computer Vision project** where the bird is controlled entirely through **hand gestures detected via webcam**.

No keyboard. No mouse. Just your fist. ✊

---

## 🎮 How to Play

| Gesture | Action |
|---|---|
| ✋ Open Palm | Bird falls (no action) |
| ✊ Closed Fist | Bird jumps! |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Unity + C#** | Game engine and bird physics |
| **Python 3** | Gesture detection controller |
| **OpenCV** | Webcam video capture |
| **MediaPipe** | Hand landmark detection (21 points) |
| **UDP Sockets** | Real-time communication between Python and Unity |

---

## 🧠 How It Works
```
Webcam → OpenCV → MediaPipe → Fist Detection → UDP Socket → Unity → Bird Jumps
```

1. Python captures webcam frames using **OpenCV**
2. **MediaPipe** detects 21 hand landmarks in real time
3. Finger tip vs knuckle positions determine if hand is a **fist or open palm**
4. On fist detection, a `JUMP` message is sent to Unity via **UDP socket on port 5065**
5. Unity's `BirdScript` listens on the socket and triggers the jump instantly
6. The gesture controller **auto-launches** when you press Play in Unity

---

## 🚀 Getting Started

### Prerequisites
- macOS (the auto-launcher uses macOS Terminal)
- Python 3.x
- Unity (any recent version)
- A webcam

### Step 1 — Clone the repo
```bash
git clone https://github.com/Vedamsh27/Retro-Flapper.git
cd Retro-Flapper
```

### Step 2 — Set up the gesture controller
```bash
cd GestureController
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3 — Download the hand tracking model
Download `hand_landmarker.task` (~29MB) from:
👉 [MediaPipe Hand Landmarker Model](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task)

Place it inside the `GestureController/` folder.

### Step 4 — Open Unity project
Open the root folder in Unity Hub and press **Play** ▶️

The gesture controller launches automatically — show your fist to jump!

---

## 📁 Project Structure
```
Retro-Flapper/
├── Assets/
│   └── Scripts/
│       ├── BirdScript.cs        ← Bird physics + gesture socket listener
│       ├── LogicScript.cs       ← Game logic & score
│       ├── PipeMoveScript.cs    ← Pipe movement
│       ├── PipeSpawnScript.cs   ← Pipe spawning
│       └── PipeMiddleScript.cs  ← Score detection
├── GestureController/
│   ├── gesture_control.py       ← Main AI gesture detection script
│   └── requirements.txt         ← Python dependencies
├── ProjectSettings/
└── README.md
```

---

## 🎯 Features

- ✅ Classic Flappy Bird gameplay with Angry Bird character
- ✅ Real-time hand gesture control via webcam
- ✅ AI fist detection using MediaPipe's 21-point hand landmarks
- ✅ Gesture smoothing — prevents accidental jumps
- ✅ UDP socket communication — no focus stealing
- ✅ Auto-launches gesture controller on game start
- ✅ Auto-cleanup on game quit
- ✅ Dynamic neon city backgrounds
- ✅ Score tracking

---

## 🔬 Gesture Detection Logic

MediaPipe detects **21 hand landmarks**. We compare fingertip positions vs knuckle positions:
```python
def is_fist(landmarks):
    tips     = [8, 12, 16, 20]   # Fingertips
    knuckles = [6, 10, 14, 18]   # Middle knuckles
    for tip, knuckle in zip(tips, knuckles):
        if landmarks[tip].y < landmarks[knuckle].y:
            return False          # Finger is open
    return True                   # All fingers curled = fist ✊
```

---

## 📦 Dependencies
```
opencv-python
mediapipe
pyautogui
```

---

## 🙏 Acknowledgements

- [MediaPipe](https://developers.google.com/mediapipe) by Google for hand tracking
- [OpenCV](https://opencv.org/) for webcam capture
- Unity for the game engine

---

## 👨‍💻 Author

**Vedamsh Cheripelli**
[GitHub](https://github.com/Vedamsh27)