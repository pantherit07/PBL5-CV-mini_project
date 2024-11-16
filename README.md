# Air Canvas: Virtual Drawing with Hand Gestures

**Air Canvas** is an interactive application that allows users to draw on a virtual canvas using hand gestures. By leveraging MediaPipe for hand tracking, this project provides a unique experience of creating digital art without touching any screen. Users can control the brush size, color, and even switch between drawing and erasing modes using their hand movements and keyboard shortcuts.

## Features

- **Hand Gesture Drawing**: Use your hands to draw on the canvas with real-time tracking via MediaPipe.
- **Customizable Brush**: Change brush size and color for varied drawing experiences.
- **Erase Mode**: Switch to an eraser to remove strokes from the canvas.
- **Multiple Drawing Areas**: Toggle between different predefined drawing areas.
- **Keyboard Shortcuts**: Control the application easily with intuitive keyboard shortcuts.
- **Save Drawings**: Capture and save your creations with timestamps.

## Requirements

Before running the project, make sure you have the following installed:

- Python 3.x
- OpenCV
- MediaPipe
- NumPy

You can install the required dependencies using the following commands:

```bash
pip install opencv-python mediapipe numpy
```

## How It Works

1. **Hand Tracking**: The application uses **MediaPipe** to track the user's hand in real time via webcam input. The position of the index finger is used to control the brush on the canvas.
   
2. **Drawing**: When the user moves their index finger in the drawing area, a colored stroke is drawn. The brush size can be adjusted, and different colors are available.

3. **Eraser Mode**: When eraser mode is toggled, moving the index finger inside the drawing area will remove strokes, simulating an eraser.

4. **Drawing Area Size**: The user can toggle between multiple predefined sizes of the drawing area using a keyboard shortcut.

5. **Saving Drawings**: After creating a masterpiece, users can save their drawing to disk. Each saved file is timestamped for easy identification.

## Keyboard Shortcuts

| Key | Action |
| --- | ------ |
| `e` | Erase Canvas |
| `c` | Change Brush Color |
| `+` | Increase Brush Size |
| `-` | Decrease Brush Size |
| `s` | Save Drawing |
| `t` | Toggle Eraser Mode |
| `q` | Quit Application |
| `d` | Toggle Drawing Area Size |

## How to Use

1. **Start the Application**: Run the script in your terminal or IDE.

2. **Use Hand Gestures**:
   - Draw by moving your index finger inside the predefined drawing area.
   - Switch to eraser mode by pressing the `t` key and erase by moving your finger in the drawing area.
   
3. **Adjust Brush Settings**:
   - Press `+` to increase the brush size and `-` to decrease it.
   - Press `c` to change the brush color.
   
4. **Save Your Drawing**: Press `s` to save your drawing. The saved file will include a timestamp in the filename for easy retrieval.

5. **Switch Drawing Areas**: Press `d` to toggle between different drawing areas of varying sizes.

6. **Exit the Application**: Press `q` to quit the application.

