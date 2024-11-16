import cv2
import mediapipe as mp
import numpy as np
import time

drawing_area_sizes = [
    (200, 150, 1080, 570),  # Size 1
    (100, 100, 1180, 620),  # Size 2
    (50, 50, 1230, 670)     # Size 3
]

def get_initial_drawing_area_size():
    return drawing_area_sizes[0]

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

current_area_index = 0
draw_area_coords = drawing_area_sizes[current_area_index]
draw_area_top_left = (draw_area_coords[0], draw_area_coords[1])
draw_area_bottom_right = (draw_area_coords[2], draw_area_coords[3])

canvas_width = 1280
canvas_height = 720
canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

draw_area_color = (255, 0, 0)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, canvas_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, canvas_height)

brush_sizes = [5, 10, 15, 20]
brush_colors = [
    (0, 255, 0),  
    (255, 0, 0),  
    (0, 0, 255), 
    (255, 255, 0), 
    (255, 165, 0),
    (128, 0, 128),
    (255, 192, 203),
    (0, 255, 255),
]
current_brush_size_index = 0
current_brush_color_index = 0

eraser_mode = False

def erase_canvas():
    global canvas
    canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

def save_drawing():
    global canvas
    x1, y1 = draw_area_top_left
    x2, y2 = draw_area_bottom_right
    cropped_canvas = canvas[y1:y2, x1:x2]
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"/Users/Ritesh/Desktop/New folder/air_canvas_drawing_{timestamp}.png"
    
    cv2.imwrite(filename, cropped_canvas)
    print(f"Drawing saved as {filename}")

def is_fist(hand_landmarks):
    finger_tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP,
    ]
    for tip in finger_tips:
        tip_y = hand_landmarks.landmark[tip].y
        base_y = hand_landmarks.landmark[tip - 2].y
        if tip_y < base_y:  
            return False
    return True

def display_instructions(frame):
    instructions = [
        "Keyboard Shortcuts:",
        "'e' - Erase Canvas",
        "'c' - Change Brush Color",
        "'+' - Increase Brush Size",
        "'-' - Decrease Brush Size",
        "'s' - Save Drawing",
        "'t' - Toggle Eraser Mode",
        "'q' - Quit",
        "'d' - Toggle Drawing Area Size"
    ]
    
    for i, text in enumerate(instructions):
        cv2.putText(frame, text, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    cv2.rectangle(frame, draw_area_top_left, draw_area_bottom_right, draw_area_color, 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, _ = frame.shape
            x = int(index_finger_tip.x * w)
            y = int(index_finger_tip.y * h)

            if is_fist(hand_landmarks):
                drawing = False
            else:
                if index_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y:
                    drawing = True
                else:
                    drawing = False

            if eraser_mode:
                if (draw_area_top_left[0] <= x <= draw_area_bottom_right[0]) and (draw_area_top_left[1] <= y <= draw_area_bottom_right[1]):
                    cv2.circle(canvas, (x, y), brush_sizes[current_brush_size_index], (0, 0, 0), -1)  # Use black for erasing
            elif drawing and (draw_area_top_left[0] <= x <= draw_area_bottom_right[0]) and (draw_area_top_left[1] <= y <= draw_area_bottom_right[1]):
                cv2.circle(canvas, (x, y), brush_sizes[current_brush_size_index], brush_colors[current_brush_color_index], -1)

    combined_display = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
    display_instructions(combined_display) 
    cv2.imshow('Air Canvas', combined_display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('e'):
        erase_canvas()
    elif key == ord('c'):
        current_brush_color_index = (current_brush_color_index + 1) % len(brush_colors)
        print(f"Brush color changed to: {brush_colors[current_brush_color_index]}")
    elif key == ord('+'):
        current_brush_size_index = (current_brush_size_index + 1) % len(brush_sizes)
        print(f"Brush size increased to: {brush_sizes[current_brush_size_index]}")
    elif key == ord('-'):
        current_brush_size_index = (current_brush_size_index - 1) % len(brush_sizes)
        print(f"Brush size decreased to: {brush_sizes[current_brush_size_index]}")
    elif key == ord('s'):
        save_drawing()
    elif key == ord('t'):
        eraser_mode = not eraser_mode
        mode = "Eraser" if eraser_mode else "Drawing"
        print(f"Switched to {mode} mode.")
    elif key == ord('d'):
        current_area_index = (current_area_index + 1) % len(drawing_area_sizes)
        draw_area_coords = drawing_area_sizes[current_area_index]
        draw_area_top_left = (draw_area_coords[0], draw_area_coords[1])
        draw_area_bottom_right = (draw_area_coords[2], draw_area_coords[3])
        print(f"Drawing area size changed to: {draw_area_coords}")

cap.release()
cv2.destroyAllWindows()