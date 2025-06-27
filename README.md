# ✨ Virtual Air Sketching with OpenCV, Flask, and Tkinter ✨

**VirtualAirSketching.py** is an interactive air-drawing application that lets users sketch in the air using a colored object tracked by their webcam. The project combines **OpenCV** for real-time video processing, **Flask** for a web interface, and **Tkinter** for save confirmation dialogs.

---

## 🎨 Key Features

✅ Draw virtually in the air using a colored marker or object  
✅ Change drawing colors (Blue, Green, Red, Yellow)  
✅ Clear the entire canvas with a simple gesture  
✅ Save your artwork as `.png` and `.pdf` files  
✅ HSV sliders for adjusting color detection dynamically  
✅ Save confirmation pop-up using Tkinter  
✅ Flask web server with basic frontend (expandable)  

---

## 📂 Project Structure

├── VirtualAirSketching.py # Main Python application script
├── frontend.html # HTML file for Flask route (placeholder)
├── drawing.png # Drawing saved as PNG (after Save button)
├── drawing.pdf # Drawing saved as PDF (after Save button)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x  
- Webcam  

### Required Libraries

Install the dependencies with:

pip install numpy opencv-python flask pillow

🖥️ How to Run
Clone the repository:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Run the application:

python VirtualAirSketching.py
The application will:

✅ Open your webcam
✅ Launch OpenCV windows for drawing and color detection
✅ Start a Flask server at http://127.0.0.1:5000

## 🕹️ How to Use
Hold a colored object in front of your webcam (green works well by default).

Adjust HSV trackbars in the Color detectors window if detection isn't accurate.

Interact with the top buttons on the screen:

CLEAR: Clears the entire drawing

Blue, Green, Red, Yellow: Change the drawing color

SAVE: Saves your canvas as drawing.png and drawing.pdf

Drawing occurs when the object moves away from the button area.

A Tkinter pop-up confirms the successful save.

Press q to quit the application.

## ⚙️ Technologies Used
OpenCV: Real-time computer vision for color tracking

Flask: Lightweight web server for future web integration

Tkinter: GUI-based save confirmation

Pillow: Image processing and PDF generation

NumPy: Numerical operations for efficient processing

## 🌟 Future Improvements
Full-featured web interface for viewing saved sketches

More drawing tools (eraser, shapes, brush sizes)

Gesture or voice control

Multi-color simultaneous drawing

## 🙋 Author
Developed by Ranjitha Narasimhamurthy
Virtual Air Drawing using real-time color tracking and gesture interaction.


