import cv2
import mediapipe as mp
import pyautogui
import math
import time

# Mouse settings
pyautogui.FAILSAFE = True
screen_w, screen_h = pyautogui.size()

# --- SMOOTHING SETUP ---
prev_ix, prev_iy = 0, 0
smooth_factor = 0.5 # 0.1 se 0.9 tak. Jitna kam hoga utna smoother but thoda slow (default 0.5 best hai)
dead_zone = 5       # Utne pixels ki movement ko ignore karenge shakiness kam karne ke liye

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
cap = cv2.VideoCapture(0)

# Window settings to make it small and out of the way
cv2.namedWindow("Educore Master Control", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Educore Master Control", 300, 200)

print("🚀 Educore Pro Smooth Mode Active!")
print("☝️ Index: Cursor | 🤏 Pinch: CLICK | 👉 Middle Up/Down: Scroll")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Points for Cursor (Index=8), Click (Thumb=4, Index=8), Scroll (Middle=12)
            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]
            middle = hand_landmarks.landmark[12]

            # --- 1. SMOOTH MOUSE CURSOR MOVEMENT ---
            # Raw screen coordinates
            target_ix, target_iy = int(index.x * screen_w), int(index.y * screen_h)
            
            # Apply Smoothing (prev * weight + current * weight)
            # prev_ix * (1 - smooth_factor) gives more weight to the past, making it smooth but lags.
            # target_ix * smooth_factor gives weight to the current position.
            curr_ix = int(prev_ix * (1 - smooth_factor) + target_ix * smooth_factor)
            curr_iy = int(prev_iy * (1 - smooth_factor) + target_iy * smooth_factor)
            
            # Use Dead Zone: Only move if the distance is greater than the zone
            if abs(curr_ix - prev_ix) > dead_zone or abs(curr_iy - prev_iy) > dead_zone:
                pyautogui.moveTo(curr_ix, curr_iy, _pause=False)
                # Store the current as previous for next frame
                prev_ix, prev_iy = curr_ix, curr_iy

            # --- 2. CLICK LOGIC ---
            # Distance between thumb and index tips
            distance = math.sqrt((index.x - thumb.x)**2 + (index.y - thumb.y)**2)
            
            if distance < 0.04: # If fingers are close enough
                pyautogui.click()
                print("🖱️ CLICKED!")
                cv2.putText(frame, "CLICK", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # Fail-safe pause to prevent double-click or stuck clicking
                pyautogui.sleep(0.3) 
                
                # Small pause after click to prevent multiple accidental clicks
                # During this pause, the code below is ignored
                continue 

            # --- 3. SCROLL LOGIC (Smooth but Fast) ---
            # Logic: If Middle finger is well above the index base, Scroll Up
            if middle.y < hand_landmarks.landmark[9].y - 0.1: # Middle UP (using knuckle reference)
                pyautogui.scroll(500) # Value badha di hai for faster dashboard scrolling
                # print("⬆️ Scrolling UP")
            # If Middle finger is well below the index base, Scroll Down
            elif middle.y > hand_landmarks.landmark[9].y + 0.1: # Middle DOWN
                pyautogui.scroll(-500)
                # print("⬇️ Scrolling DOWN")

    # Display small window
    cv2.imshow("Educore Master Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()