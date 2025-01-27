# Eye Care System 👀

## Overview

The Eye Care System is a Python-based application that uses computer vision to monitor eye health and provide real-time alerts for eye strain and prolonged eye closure. It uses webcam tracking to analyze eye movements and provide timely notifications.

## Features

- 📹 Real-time eye tracking using webcam
- 🚨 Blink reminders for prolonged eye opening
- 🔔 Alarm for extended eye closure
- 📊 Live visualization of eye aspect ratio

## Requirements

- Python 3.7+
- OpenCV
- CVZone
- Plyer
- Pygame

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Kshitiz19215/Aankhe.git
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure you have an `Alarm.wav` file in the project directory for the alarm sound.

## Usage

Run the script:
```bash
python Eye_Care.py
```

### Controls
- Press 'q' to quit the application

## How It Works

The application uses facial landmark detection to:
- Calculate the eye aspect ratio
- Detect prolonged eye opening
- Trigger desktop notifications for blinking
- Sound an alarm for extended eye closure

## Customization

You can adjust the following parameters in the code:
- `open_threshold_duration`: Time before blinking reminder
- `close_threshold_duration`: Time before eye closure alarm
- Eye aspect ratio thresholds for detection

## Dependencies

- OpenCV: Computer vision and image processing
- CVZone: Advanced face and hand tracking
- Plyer: Cross-platform desktop notifications
- Pygame: Audio playback for alarm

## Troubleshooting

- Ensure webcam is properly connected
- Check that all dependencies are installed
- Verify `Alarm.wav` is in the correct directory

## Disclaimer

This is a health assistance tool and should not replace professional medical advice.

## Author

[Vishishta Mary Kumar]
