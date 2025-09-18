# Simple Text-to-Video (TTV) AI

A Python-based project that converts text into video with audio narration. This project uses **Pillow** for image/font handling, **pydub** for audio processing, and **MoviePy** for video creation.  

---

## Features

- Convert plain text into a video with spoken audio.  
- Support for custom fonts and text styling.  
- Generates MP4 video output with background audio.  
- Easy to extend for different text-to-speech engines or visual styles.

---

## Requirements

- Python 3.7+  
- `pip` >= 24.x (upgrade recommended)  
- **FFmpeg** installed and added to your system PATH  
- Libraries:
  ```bash
  pip install -r requirements.txt

---

## Usage

```bash
python text_to_video.py input.txt output.mp4
