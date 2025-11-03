# 🎥 VisT — The Visual Terminal

**VisT** (Visual Terminal) is a command-line powerhouse that turns your terminal into a creative visual environment.  
Built entirely using **pure Python**, VisT brings together **art, analytics, gaming, and multimedia** — all without a single framework or GUI dependency.

---

## ⚙️ Hackathon Constraint

> **Rules we followed:**
> - No frameworks or GUIs (HTML/CSS/JS disallowed)  
> - Only core programming and libraries (OpenCV, CuPy, Pygame allowed)  
> - Maximum 500 lines  
> - Must handle invalid input gracefully  
> - Demonstrate structure, creativity, and simplicity  
> - Runs completely in CLI  
> - Windows + Python 3.13 compatible

---

## 🚀 Modes Overview

VisT features **4 dynamic modes**:

### 🖼️ 1. Image → ASCII Art
Convert any image into ASCII art directly in your terminal.  
- **Modes:**  
  - Default  
  - Edit  
- **Display Options:**  
  - Black & White  
  - RGB Color  

### 📊 2. Data Visualization
A powerful **text-based data graph generator** with 3 styles:
1. **Bar Chart** — simple comparative bars  
   - Example input: `India:120,USA:90,Japan:70,Germany:60,Brazil:50`
2. **Line Graph** — plot value trends  
   - Example input: `100,120,90,80,60,70,110`
3. **Pie Chart** — visualize percentages  
   - Example input: `Food:40,Transport:25,Rent:20,Other:15`

### 🦖 3. Raptors Go! (Mini Game)
An interactive **CLI survival game** where your reflexes are tested as you dodge obstacles and rack up points.

### 🎬 4. ASCII Movie Player (Main Highlight)
Play real videos as ASCII art with synced **audio playback** and **GPU acceleration**!  
- Supports **native FPS video playback** (no 24 fps lock)  
- **Audio sync via pygame mixer**  
- **GPU acceleration** using CuPy + OpenCV CUDA  
- **Pause/Resume** with spacebar  
- Displays GPU status: `"GPU Active"` / `"No GPU Detected"`

---

## 🧠 Unique Selling Point (USP)

> “Turning your terminal into a creative multimedia space — powered by GPU.”

Unlike any traditional CLI tool, VisT merges **graphics, sound, and interactivity** all in a terminal environment.  
Mode 4 (ASCII Movie Player) is the highlight — blending visual art and computation into one unified experience.

---

## 🛠️ Installation

### 1️⃣ Prerequisites
- Python 3.13+
- Windows OS
- FFmpeg installed and added to PATH

### 2️⃣ Install Dependencies
```bash
pip install opencv-python-headless cupy-cuda12x pygame numpy
